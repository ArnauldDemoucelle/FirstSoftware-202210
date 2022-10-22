########################################
#
# “你帮我助”小软件
# 物品交换软件
# 可以添加物品的信息，删除物品的信息，显示物品列表， 也可以查找物品的信息
#
# Written by Arnauld Demoucelle
# Version 1.0.0
# October 2022
#
########################################


import pandas as pd
import os
import sys


# 把物品列表从数据库（Excel表格）导入到DataFrame。
# 如果数据库（Excel表格）存在，用其数据。
# 如果数据库不存在，创建空的DataFrame。
def GetData():
    storageFile = 'ArticlesData.xlsx'
    if os.path.exists(storageFile):
        articlesList = pd.read_excel(storageFile)
    else:
        articlesList = pd.DataFrame(columns=['Name', 'Amount'])
    StartingScreen(articlesList)


# 给用户显示选项。
# 其他函数运行完时，将再调用StartingScreen函数，重新给用户显示选项。
def StartingScreen(articlesList):
    print(" ")
    print("What would you like to do?")
    print(" - Press 1 to see the list of all articles.")
    print(" - Press 2 to look up a specific article.")
    print(" - Press 3 to add an article.")
    print(" - Press 4 to exit the program.")
    print(" ")
    GetInput(articlesList)


# 用户输入一个int，选择想使用的功能。
# 根据用户的选择，调用相应的函数。
# 如果用户的输入不是可供选项，让其重新输入。
def GetInput(articlesList):
    x = int(input())
    if x == 1:
        PrintList(articlesList)
    if x == 2:
        SearchArticle(articlesList)
    if x == 3:
        AddArticleDirectly(articlesList)
    if x == 4:
        SaveAndExit(articlesList)
    else:
        print('Please try again.')
        GetInput(articlesList)


# 显示物品列表。
# 返回到StartingScreen函数。
def PrintList(articlesList):
    print("The list of current articles:")
    print(articlesList)
    StartingScreen(articlesList)


# 查找物品的信息。
# 用户输入物品名。
# 查找了物品后，将给用户提供添加和删除选项。
# 如果物品在列表中，可以添加或删除该物品。
# 如果物品不在列表中，只能添加物品。
# 添加和删除都将调用对应的函数。
def SearchArticle(articlesList):
    print("Please type in the name of the article you would like to search for.")
    articleName = input()
    if articleName in articlesList['Name'].values:
        print("Item found.")
        print(articlesList.loc[articlesList['Name'] == articleName])
        print("Would you like to delete this item? y/n")
        x = input()
        if x == 'y':
            DeleteArticle(articlesList, articleName)
        else:
            print("Would you like to add to this item? y/n")
            x = input()
            if x == 'y':
                AddFromFound(articlesList, articleName)
            else:
                StartingScreen(articlesList)
    else:
        print("Item not found.")
        print("Would you like to add this item? y/n")
        x = input()
        if x == 'y':
            AddFromNotFound(articlesList, articleName)
        if x == 'n':
            StartingScreen(articlesList)


# 添加物品。
# 如果用户在GetInput()函数选择添加物品，将调用这个函数。
# 用户输入物品名，程序检查物品表中是否有这项物品。
# 根据物品是否在列表中，将调用相应的添加函数。
def AddArticleDirectly(articlesList):
    print("Which article would you like to add?")
    articleName = input()
    if articleName in articlesList['Name'].values:
        print("Item found.")
        AddFromFound(articlesList, articleName)
    else:
        print("Item not yet on the system.")
        AddFromNotFound(articlesList, articleName)


# 添加已有物品的数量。
# 用户输入想要添加的数量。
def AddFromFound(articlesList, articleName):
    index = articlesList.index[articlesList['Name'] == articleName][0]
    print(articlesList.loc[articlesList['Name'] == articleName])
    print("How many would you like to add?")
    x = int(input())
    articlesList.iat[index, 1] = articlesList.iat[index, 1] + x
    print("Added successfully.")
    print(articlesList.loc[articlesList['Name'] == articleName])
    StartingScreen(articlesList)


# 添加列表中尚没有的物品。
# 物品在列表的最后被添加。
# 用户输入想要增加的数量。
def AddFromNotFound(articlesList, articleName):
    index = len(articlesList.index)
    print("How many would you like to add?")
    x = int(input())
    articlesList.loc[index] = [articleName, x]
    print("Added successfully")
    print(articlesList.loc[articlesList['Name'] == articleName])
    StartingScreen(articlesList)


# 删除已有物品的一定数量。
# 用户输入想要删除的数量。
def DeleteArticle(articlesList, articleName):
    index = articlesList.index[articlesList['Name'] == articleName][0]
    print("How many would you like to delete?")
    x = int(input())
    articlesList.iat[index, 1] = articlesList.iat[index, 1] - x
    print("Deleted successfully.")
    print(articlesList.loc[articlesList['Name'] == articleName])
    StartingScreen(articlesList)


# 当用户选择退出程序，物品列表被保存到数据库（Excel表格）。
def SaveAndExit(articlesList):
    articlesList.to_excel('ArticlesData.xlsx', columns=['Name', 'Amount'], index=False)
    sys.exit()


# 程序首先运用GetData()函数。
if __name__ == "__main__":
    GetData()
