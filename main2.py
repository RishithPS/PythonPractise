# email = "baraa@gmail.com"

# if email == "":
#     print("email must not be empty")
# elif "@" not in email and "." in email:
#     print("email must contain a . or @")
# elif email.count("@") != 1:
#     print("email must contain only one @ symbol")
# elif not email.endswith((".com", ".org", ".net")):
#     print("email should end with .com or .org or .net")
# elif len(email) > 254:
#     print("email must not be longer than 254 characters")
# elif not (email[0].isalnum() and email[-1].isalnum()):
#     print("email must start and end with a letter or a digit")
# else:
#     print("the email is valid")

# state = "Andhra pradesh"

# match state:password = "Siddyaef"

# if password == "":
#     print("password must not be empty")
# elif len(password) != 8:
#     print("password must at least be 8 characters long")
# elif (password)== 1:
#     print("nice")
# else:
#     print("asdf")
#     case "Andhra pradesh":
#         print("Ap")


# def is_one_uppercase(s):
#     return sum(c.isupper() for c in s)


# def is_one_lowercase(s):
#     return sum(c.islower() for c in s)


# password = "s234T4531s"

# if password == "":
#     print("password must not be empty")
# elif len(password) < 8:
#     print("password must at least be 8 characters long")
# elif is_one_uppercase(password) < 1:
#     print("password should have at least one uppercase letter")
# elif is_one_lowercase(password) < 1:
#     print("password should have at least one lowercase letter")
# elif len(password) - len(password.strip()) >= 1:
#     print("password must not have any spaces")
# elif password[0].isalnum() and password[-1].isalnum():
#     print("password must start and end with a letter or a digit")
# else:
#     print("the password is valid")

i = ['serasd','qwerqwe','ascrwe','Goku']
print(i[1:3])

*details,me=i
print(details,me)

l=list('python')
print(l)
