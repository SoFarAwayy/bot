import json
import unittest

spisok_members = ["Ivan", "Petya", "Vasya"]

class Ctx:
    def id(): return "1234567890"

dictt = {"1234567890": 100}

def on_member_remove(member):
    members = len(spisok_members)
    return f'members: {members}'

def on_member_join(member):
    with open("information.json", "r") as json_file: json_dict = json.load(json_file)
    member_id = "1234567890"
    with open("information.json", "r") as json_file: 
            json_dict = json.load(json_file)

            json_dict["information"][member_id] = {"been": 1}

            json_dict["information"][member_id].update({"royals": 10})

            json_dict["information"][member_id].update({"invites": 0})

            json_dict["information"][member_id].update({"time": []})

            with open("information.json", "w") as json_file:
                json.dump(json_dict, json_file, indent=4)
    return json_dict

def get_user_royals(ctx: Ctx):
    return dictt[ctx.id]

class Test(unittest.TestCase):
    def test_1_single(self):
        self.assertEqual(on_member_remove("Vasya"), 'members: 3')

    def test_2(self):
        self.assertEqual(on_member_join("Vasya"), "{'information': {'159985870458322944': {'nickname': 'MEE6', 'been': 1, 'royals': 10, 'invites': 0, 'time': []}, '854662130682691585': {'nickname': '_sofaraway_', 'been': 1, 'royals': 230, 'invites': 0, 'time': []}, '1123746955974152272': {'nickname': 'RoyalRust', 'been': 1, 'royals': 10, 'invites': 0, 'time': []}, '1205622520284323971': {'nickname': 'badb0yyy12', 'been': 2, 'royals': 1100, 'invites': 0, 'time': []}, '204255221017214977': {'been': 1, 'royals': 10, 'invites': 0, 'time': []}, '472911936951156740': {'been': 1, 'royals': 10, 'invites': 0, 'time': []}, '557628352828014614': {'been': 1, 'royals': 10, 'invites': 0, 'time': []}, '1274696363967385630': {'been': 1, 'royals': 545, 'invites': 0, 'time': []}, '1234567890': {'been': 1, 'royals': 10, 'invites': 0, 'time': []}}, 'games': {'duels': {'duel 1': {'message_id': 1280909072228552768, 'stavka': 50, 'players': 1, 'first player nickname': 'SoFarAway', 'first player id': 854662130682691585}}}, 'shop': {'message_id': 1317199135321100461}}")

    def test_3(self):
        self.assertEqual(get_user_royals(Ctx()), 100)

if __name__ == "__main__":
    unittest.main()
