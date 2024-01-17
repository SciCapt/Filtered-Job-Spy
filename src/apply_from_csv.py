from pandas import read_csv
from webbrowser import open as open_page
from os import getcwd

def get_last_substring_index(string:str, substring='\\'):
    index = 0
    while True:
        try:
            index = string.index(substring, index+1)
        except:
            return index

try:
    # Get data from a previous filtered search in CWD
    filename = 'filtered_search.csv'
    jobs = read_csv(filename)

except:
    try:
        # Get data from a previous filtered search one dir up
        CWD = str(getcwd())
        CWD_oneup = CWD[:get_last_substring_index(CWD)+1]
        jobs = read_csv(f"{CWD_oneup}{filename}")

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

# Reset jobs index
jobs.index = [*range(len(jobs))]

# Iterate through jobs, applying to ones wanted to
finished_looking = False
for ind in jobs.index[::-1]:
    # Print current job info
    print(f"Job #{ind+1}:")
    print(f"Title: {jobs['title'][ind]}")
    print(f"Location: {jobs['location'][ind]}")
    print(f"Salary: ${jobs['min_amount'][ind]}-${jobs['max_amount'][ind]}")
    print(f"Company: {jobs['company'][ind]}")

    do_apply = input("Apply to job (skips otherwise)? (y/n): ")

    # Check if wants to apply to current job
    if do_apply.lower().__contains__('y'):
        open_page(jobs['job_url'][ind])

        see_next = input("See next job? (y/n): ")

        # Display next job after applying to current job, delete current job
        if see_next.lower().__contains__('y'):
            print("Displaying next job ...\n")
            jobs = jobs.drop(ind)
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
            jobs = jobs.drop(ind)
            continue
        
        # Stops going through the jobs list
        else:
            print("Stopping!\n")
            finished_looking = True
            break

# Update jobs csv (with deleted/finished ones)
jobs.to_csv('filtered_search.csv')

# Finished
if not finished_looking:
    print("No Jobs left to display!\n")