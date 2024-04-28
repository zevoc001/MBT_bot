from DataBase import add_user
import unittest


class DataBaseUnittest(unittest.TestCase):
    def test_add_user(self):
        user = {
            "telegram_id": "string",
            "access": "string",
            "data_reg": "2024-04-22",
            "status": "string",
            "rating": 0,
            "profit": 0,
            "offers": 0,
            "comment": "string",
            "name": "string",
            "sex": "string",
            "born": "2024-04-22",
            "age": 0,
            "residence": "string",
            "education": "string",
            "course": 0,
            "profession": "string",
            "salary": 0,
            "hard_work": True,
            "mid_work": True,
            "art_work": True,
            "other_work": "string",
            "tools": "string",
            "language": "string",
            "phone": "string",
            "email": "string",
            "citizenship": "string",
            "wallet": "string",
            "is_driver": True,
            "transport": "string",
            "is_military": True,
            "other_info": "string"
        }
        result = add_user(user)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
