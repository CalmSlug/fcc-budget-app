class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
        self.balance = 0
        
    def __str__(self):
        str1 = ""
        str2 = ""
        str3 = ""

        str1 += "{:*^30}".format(self.name)
        str1 += "\n"
        
        for i in self.ledger:
            str2 += "{:23}".format(i["description"][0:23])
            str2 += "{:7.2f}".format(i["amount"])
            str2 += "\n"

        str3 += "Total: "
        str3 += "{:.2f}".format(self.balance)
        return str1 + str2 + str3


    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
        self.balance += amount

    def get_balance(self):
        return self.balance

    def check_funds(self, amount):
        if amount <= self.balance:
            return True
        else:
            return False

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            self.balance -= amount
            return True
        else:
            return False

    def transfer(self, amount, category):
        if self.withdraw(amount, f"Transfer to {category.name}"):
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        else:
            return False


def create_spend_chart(categories):
    output = []
    output.append("Percentage spent by category")

    cnt = 100
    while cnt >= 0:
        str = ""
        str += "{:3}".format(cnt)
        str += "| "
        str += " " * len(categories) * 3
        output.append(str)
        cnt -= 10

    amount_full = 0
    for cat in categories:
        for i in cat.ledger:
            if i["amount"] < 0:
                amount_full += -i["amount"]
    percents = []
    for cat in categories:
        amount_sub = 0
        for i in cat.ledger:
            if i["amount"] < 0:
                amount_sub += -i["amount"]
        percents.append(int(amount_sub / amount_full * 10) + 1)
    cnt = 0
    for prc in percents:
        for i in range(prc):
            output[11 - i] = output[11 - i][:5 + cnt] + "o" + output[11 - i][6 + cnt:]
        cnt += 3

    output.append("    -" + "-" * len(categories) * 3)

    lst_len = []
    for cat in categories:
        lst_len.append(len(cat.name))
    for i in range(max(lst_len)):
        output.append("     " + " " * len(categories) * 3)

    lst_names = []
    for cat in categories:
        lst_names.append(cat.name)
    cnt = 0
    for name in lst_names:
        mv_dw = 0
        for letter in name:
            output[13 + mv_dw] = output[13 + mv_dw][:5 + cnt] + letter + output[13 + mv_dw][6 + cnt:]
            mv_dw += 1
        cnt += 3

    return "\n".join(output)


# Output showcase
food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
clothing = Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)
auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)

print(food, "\n")
print(create_spend_chart([food, clothing, auto]))