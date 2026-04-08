answer=''
i=1
while i<=3:
    answer= input('do you agree(yes/no):')
    if answer=='yes':
        print('Glad we are on the same page')
        break
    i+=1
else:
    print('3 strikes,you are out')

