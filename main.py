import sqlite3
from typing import Final, List, FrozenSet, Optional, Tuple, Union

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
import uvicorn


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


with sqlite3.connect('db/sqlite3/features.sqlite3') as conn:
    cur = conn.cursor()
    cur.execute("select code from features;")
    available_utf16codes: FrozenSet[str] = frozenset(i[0] for i in cur.fetchall())  # unpack tuple
    cur.close()


@app.get('/')
async def root(request: Request, search_char: Optional[str] = None):
    if search_char is None or search_char == "":
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "res": None,
                "input_char": None,
                "input_code": None,
                "reccomend_end": None,
            }
        )

    if len(search_char) != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found"
        )

    if char_to_code(search_char, "utf-16be") not in available_utf16codes:
        print(char_to_code(search_char, "utf-16be"))
        return templates.TemplateResponse('unavailable.html', {"request": request,})

    ranking = cos_sims_ranking(search_char)
    reccomend_end = sum(float(elm[2]) > 95 for elm in ranking[:6])  # Over 95% (6 items at most)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "res": cos_sims_ranking(search_char),
            "input_char": search_char,
            "input_code": char_to_code(search_char, "utf-8", lower=False),
            "reccomend_end": reccomend_end,
        }
    )


def select_rows_by_label(char_label: int) -> List[Tuple[Union[float, str]]]:
    with sqlite3.connect('db/sqlite3/features.sqlite3') as conn:
        cur = conn.cursor()
        cur.execute("""
            select
                feature_0, feature_1, feature_2,  feature_3,  feature_4,  feature_5,  feature_6,  feature_7,
                feature_8, feature_9, feature_10, feature_11, feature_12, feature_13, feature_14, feature_15,
                code
            from features
            where label = ?;
        """, (char_label,))
        res = cur.fetchall()
        cur.close
        return res


def select_feature_label_by_code(char_code: str) -> Tuple[np.ndarray, int]:
    with sqlite3.connect('db/sqlite3/features.sqlite3') as conn:
        cur = conn.cursor()
        cur.execute("""
            select
                feature_0, feature_1, feature_2,  feature_3,  feature_4,  feature_5,  feature_6,  feature_7,
                feature_8, feature_9, feature_10, feature_11, feature_12, feature_13, feature_14, feature_15,
                label
            from features
            where code = ?;
        """, (char_code,))
        res = cur.fetchone()
        cur.close()
        return np.asarray(res[:16]), res[16]


def cos_sims_ranking(search_char: str) -> List[Tuple[str, str, str]]:
    res = []
    char_code = char_to_code(search_char, "utf-16be")
    char_vec: Final[np.ndarray]
    char_vec, char_label = select_feature_label_by_code(char_code)

    for row in select_rows_by_label(char_label):
        v1 = row[0:16]
        cos_sim = np.dot(v1, char_vec) / (np.linalg.norm(v1) * np.linalg.norm(char_vec))
        res.append((cos_sim, row[16]))
    
    res.sort(reverse=True)
    return [(chr(int('0x' + code, base=16)), utf16code_to_utf8code(code), '%0.4f' % (score * 100)) for (score, code) in res[:50]]


def char_to_code(char: str, enc: str, lower: bool = True) -> str:
    if lower:
        return "".join("{:02x}".format(c) for c in char.encode(enc))
    return "".join("{:02X}".format(c) for c in char.encode(enc))


def utf16code_to_utf8code(utf16code: str) -> str:
    return "".join("{:02X}".format(c) for c in chr(int('0x' + utf16code, base=16)).encode("utf-8"))


if __name__ == '__main__':
    uvicorn.run(app)
