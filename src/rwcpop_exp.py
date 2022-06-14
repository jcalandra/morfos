import main_mso_char


file = main_mso_char.Path(__file__).resolve()
project_root = str(file.parents[1])
for i in range(48,101):
    if i < 10:
        number = '0' + str(i)
    else:
        number = str(i)
    test_path = project_root + '/data/rwcpop/Pop ' + number + ' (grid).csv'
    result_path = project_root + '/results/rwcpop/Pop ' + number +'/'
    pop_xx = main_mso_char.parser(test_path)
    print(pop_xx)
    main_mso_char.main(pop_xx, result_path)
