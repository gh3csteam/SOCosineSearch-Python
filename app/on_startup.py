from data_collection.data_dump import fill


def on_startup():
    while True:
        user_input = input("do you want to update your database? (Y/n) > ").strip().lower()
        match user_input:
            case "y":
                user_iterations = input("how many iterations (100 items per 1 iter, default = 100)> ")
                if (user_iterations.isdigit()) and int(user_iterations) > 0:
                    fill(iter=int(user_iterations))
                    return True
                else:
                    fill()
                    return True
            case "n":
                return True
            case _:
                print("Unknown input, please type y or n")
        