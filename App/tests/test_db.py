from database import add_user
import unittest


class DataBaseUnittest(unittest.IsolatedAsyncioTestCase):
    async def test_add_user(self):
        user = {
             "name": "\u0411\u043e\u0439\u043a\u043e \u0418\u0432\u0430\u043d "
                     "\u0410\u043d\u0430\u0442\u043e\u043b\u0435\u044c\u0432\u0438\u0447",
             "sex": "\u041c\u0443\u0436\u0441\u043a\u043e\u0439",
             "born": "2002-07-10",
             "residence": "\u0432\u0430\u043b\u043f",
             "education": "\u0412\u044b\u0441\u0448\u0435\u0435",
             "profession": "\u043f\u044b\u0432\u0430\u043f\u044b\u0432",
             "salary": 345,
             "hard_work": True,
             "mid_work": True,
             "art_work": True,
             "other_work": "\u0414\u0430",
             "tools": "\u0414\u0430",
             "phone": "+79966311910",
             "wallet": "3456345",
             "transport": "\u043d\u0435\u0442",
             "other_info": "\u043d\u0435\u0442",
             "id": "6775110868"
        }
        result = await add_user(user)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
