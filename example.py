from KIBIT import *

if __name__ == '__main__':

    u = KIBIT('http://localhost/')

    print(u.document(text='内装が綺麗でした．', document_id=1, category_id=690))
    print(u.document(text='雰囲気が良かった．', document_id=2, category_id=690))
    print(u.document(text='ここの店の杏仁豆腐は美味しい．', document_id=3, category_id=690))
    print(u.document(text='杏仁豆腐の良い塩梅な甘さを実現．', document_id=4, category_id=690))

    print(u.teacher(teacher_id=300, category_id=690, relevant_ids=[1, 2], not_relevant_ids=[3, 4]))
    print(u.result(teacher_id=300, category_id=690))
