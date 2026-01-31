# import pandas
#
# file_path = r"C:\Users\lenovo\Downloads\topic-research-20231123.xlsx"
#
# file = pandas.read_excel(file_path)
#
# for i in range(len(file["Content Idea URL"])):
#     if   pandas.notna(file["Content Idea URL"][i]):
#         print(f"{i}. {file['Content Idea URL'][i]}")
#

# table = [["Cornflakes", 1.65], ["Rice Krispies", 1.5], ["Weatablix", 1.6], ["Oatmeal", 8.33530]]
# searchItem = input("Enter the item you want to search: ")
# found = False
#
# for i in table:
#
#     if i[0] == searchItem:
#         print(f"{round(i[1], 2)}")
#         found = True
#         break
# if not found:
#     print("Item not found")

mass = int(input ("Pls enter your mass in KG: "))
height = float(input ("Pls enter your height in M: "))
bmi = mass/(height*height)
print(bmi)

if bmi < 18.5 and bmi >=16:
    print("you are underweight")
elif bmi > 18.5 and bmi <= 25:
    print("you are normal")
elif bmi > 25 and bmi <= 30:
    print("you are overweight")
elif bmi > 35:
    print("You are fat and gay")
else:
    print("you are an alien")