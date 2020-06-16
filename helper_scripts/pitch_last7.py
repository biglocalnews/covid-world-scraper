# empt_dict = {'01': '31', '02': '29', '03': '31', '04': '30', '05': '31', '06': '30', '07': '31', '08': '31', '09': '30', '10': '31', '11': '30', '12': '31'}

# date = '06_04'


def get_last_seven(date_input):

    dict_input = {'01': '31', '02': '29', '03': '31', '04': '30', '05': '31', '06': '30', '07': '31', '08': '31', 
    '09': '30', '10': '31', '11': '30', '12': '31'}

    dates_to_grab = []

    current_date = date_input.split('_')
    month = current_date[0]
    day = current_date[1]
    month_before = int(month) -1
    previous_month = f'0{month_before}'
    days_prev_month = dict_input[previous_month]

    for day_num in range(0, 7):

        curr_day = int(day) - day_num


    if int(day) >= 7:

        for day_num in range(0, 7):

            curr_day = int(day) - day_num
            curr_day = str(curr_day).zfill(2)
            file_add = f'2020-{month}-{curr_day}'
            dates_to_grab.append(file_add)

    else:

        days_left = 7 - int(day)

        for day_num in range(0, int(day)):

            curr_day = int(day) - day_num
            curr_day = str(curr_day).zfill(2)
            file_add = f'2020-{month}-{curr_day}'
            dates_to_grab.append(file_add)
            

        for day_num in range(0, days_left):

            curr_day = int(days_prev_month) - day_num
            curr_day = str(curr_day).zfill(2)
            file_add = f'2020-{previous_month}-{curr_day}'
            dates_to_grab.append(file_add)

    return dates_to_grab
      

if __name__ == '__main__':
    get_last_seven(date_input)


    


