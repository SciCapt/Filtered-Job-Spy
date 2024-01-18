from webbrowser import open as open_page
from os import getcwd

# from pandas import read_csv
import csv

def get_last_substring_index(string:str, substring='\\'):
    index = 0
    while True:
        try:
            index = string.index(substring, index+1)
        except:
            return index

def get_csv_data(filename):
    jobs = []
    with open(filename) as csv_file:
        df = csv.reader(csv_file, delimiter=',')
        for i, row in enumerate(df):
            if i:
                jobs.append(row)
            else:
                index = row
    return jobs, index

try:
    # Get data from a previous filtered search in CWD
    filename = 'filtered_search.csv'
    # jobs = read_csv(filename)

    # Using Python' CSV module
    jobs, index = get_csv_data(filename)

except:
    try:
        # Get data from a previous filtered search one dir up
        CWD = str(getcwd())
        CWD_oneup = CWD[:get_last_substring_index(CWD)+1]
        extended_filename = f"{CWD_oneup}{filename}"

        # Using pandas
        # jobs = read_csv(extended_filename)

        # Using CSV
        jobs, index = get_csv_data(extended_filename)

    except:
        print("Can't find 'filtered_search.csv'! Make sure it is in the current or the next up directory\n")
        print(f"\nCurrent Working Directory (For Context): {getcwd()}\n")
        input("Press any key to continue ...")
        raise FileNotFoundError()

## Stylish Opening Title ##
strlen = 50
print("\n" + "="*strlen)
print("=" + "## Jobs CSV Loader ##".center(strlen-2) + "=")
print("=" + "By SciCapt (GitHub)".center(strlen-2) + "=")
# print("=" + "Job Spy by Bunsly (GitHub)".center(strlen-2) + "=")
print("="*strlen + '\n')

## Step 5 - Run through jobs left and apply to them! ##
print("#### Applications Start ####\n")

# # Reset jobs index
# jobs.index = [*range(len(jobs))]

# Iterate through jobs, applying to ones wanted to
finished_looking = False
for ind in [*range(len(jobs))][::-1]:
    # Print current job info
    try:
        print(f"Job #{ind+1}:")
        print(f"Title: {jobs['title'][ind]}")
        print(f"Location: {jobs['location'][ind]}")
        print(f"Company: {jobs['company'][ind]}")
        print(f"Salary: ${jobs['min_amount'][ind]}-${jobs['max_amount'][ind]}")

    except:
        print(f"Title: {jobs[ind][0]}")
        print(f"Location: {jobs[ind][1]}")
        print(f"Company: {jobs[ind][2]}")
        min_sal = jobs[ind][3]
        max_sal = jobs[ind][4]

        # Fix not given min salary info
        try:
            min_sal = int(min_sal)
        except:
            min_sal = '???'

        # Fix not given max salary info
        try:
            max_sal = int(max_sal)
        except:
            max_sal = '???'

        print(f"Salary: ${min_sal} - ${max_sal}")

    # Get input about applying
    do_apply = input("Apply to job (skips otherwise)? (y/n): ")

    # Check if wants to apply to current job
    if do_apply.lower().__contains__('y'):
        # Pandas
        try:
            open_page(jobs['job_url'][ind])

        # Python CSV
        except:
            open_page(jobs[ind][5])

        see_next = input("See next job? (y/n): ")

        # Display next job after applying to current job, delete current job
        if see_next.lower().__contains__('y'):
            print("Displaying next job ...\n")

            # Pandas
            try:
                jobs = jobs.drop(ind)

            # Python CSV
            except:
                jobs.pop(ind)
            
            continue

        # Stop seeing jobs after applying to current one
        else:
            print("Okay, all done then!\n")
            finished_looking = True
            break

    # Didn't want to apply
    else:
        # Continues and deletes this current job
        cont = input("Continue looking through jobs? (y/n): ")
        if cont.lower().__contains__('y'):
            print("Displaying next job ...\n")

            # Pandas
            try:
                jobs = jobs.drop(ind)

            # Python CSV
            except:
                jobs.pop(ind)
            
            continue
        
        # Stops going through the jobs list
        else:
            print("Stopping!\n")
            finished_looking = True
            break

# (Pandas) Update jobs csv (with deleted/finished ones)
try:
    jobs.to_csv(filename)

# Python CSV
except:
    with open(filename, 'w', newline='') as remaining_csv:
        # Setup the writer
        writer = csv.writer(remaining_csv)

        # Setup the primary columns
        writer.writerow(index)

        # Write the remaining rows
        for row in jobs:
            writer.writerow(row)

# Finished
if not finished_looking:
    print("No Jobs left to display!\n")