import os

def files_list(country_name):

    # grabs the list of files available
    # sorts them in reverse order so that you are getting the most recent date first, then the previous day

    file_path = '/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/old_data'

    country_files = []
    for indiv_file in os.listdir(file_path):
        if country_name in indiv_file:
            country_files.append(indiv_file)

    country_files.sort(key = lambda x: x[0:11], reverse=True)

    return country_files

if __name__ == '__main__':
    files_list(country_name)