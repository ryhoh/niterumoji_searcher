import psycopg2
import pandas as pd
import numpy as np


def cos_sims(char_vec, df):
    res = []
    for idx, row in df.iterrows():
        v1 = row.iloc[0:16]
        cos_sim = np.dot(v1, char_vec) / (np.linalg.norm(v1) * np.linalg.norm(char_vec))
        res.append([cos_sim, row['Code']])
    return res


def cos_sim(vec1, vec2) -> float:
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


# def search(code):
#     search_vec = np.array(df[df['Code'] == code].iloc[:, 0:16])[0]
#     res = cos_sims(search_vec)
#     res.sort(reverse=True)
#
#     print('%s に類似する見た目の文字：' % chr(int(code, base=16)))
#
#     for (score, candidate) in res[:50]:
#         print('%s: %s  (%.6f accuracy)' % (candidate, chr(int('0x' + candidate, base=16)), score))


def main():
    df = pd.read_csv('vector.csv', index_col=0)
    df['code_i'] = 0

    for i in range(df.shape[0]):
        df.iloc[i, 17] = int('0x' + df.iloc[i, 16], base=16)

    # df['code_i'] = df['code_i'].astype(np.int32)

    # df = df.sort_values('code_i')

    order = """
    insert into feature (code, feature_idx, value)
    values (%s, %s, %s);
    """

    with psycopg2.connect(host="localhost",
                          user="maintainer",
                          password="maintainer",
                          database="similarity") as conn:
        conn.autocommit = True
        for i in range(df.shape[0]):
            print(i, end=' ')

            for j in range(16):
                # print(df.iloc[i, 17], j, df.iloc[i, j])
                with conn.cursor() as cur:
                    cur.execute(order, (int(df.iloc[i, 17]), j, df.iloc[i, j]))
                # conn.commit()


if __name__ == '__main__':
    main()
