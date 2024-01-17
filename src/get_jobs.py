# Author (Filtering): SciCapt
# GitHub: https://github.com/SciCapt
# Author (Job Spy): Bunsly
# GitHub: https://github.com/Bunsly

## Stylish Opening Title ##
strlen = 50
print("\n" + "="*strlen)
print("=" + "## Filtered Job Spy ##".center(strlen-2) + "=")
print("=" + " Filtering by SciCapt (GitHub)".center(strlen-2) + "=")
print("=" + " Job Spy by Bunsly (GitHub)".center(strlen-2) + "=")
print("="*strlen + '\n')

## User Inputs ##
# Job search params
USE_SITES = ["linkedin", "indeed", "zip_recruiter", "glassdoor"]

print(f"Using these sites: {USE_SITES}")
if input("Modify which sites are used? (y/n): ").lower().__contains__('y'):
    print("\nType the name of any site if you want to exclude it from the search")
    print("Press ENTER when done, or if none:\n")
    exclude_sites = []
    for i in range(10):
        site = input(f"Site to exclude: ").lower()
        if site in USE_SITES:
            USE_SITES.pop(USE_SITES.index(site))
        elif site == '':
            break
        else:
            print("This site is not in the current list!\n")
    print(f"Done! Using these sites: {USE_SITES}\n")

JOB_SEARCH_TITLE = input("Job Title to Search For: ")
JOB_SEARCH_LOCATION = input("Job Location Desired: ")
NUM_RESULTS_PER_SITE = input("# Results Wanted (per site): ")
if NUM_RESULTS_PER_SITE == '':
    NUM_RESULTS_PER_SITE = 20
else:
    NUM_RESULTS_PER_SITE = int(NUM_RESULTS_PER_SITE)
if 'indeed' in USE_SITES or 'glassdoor' in USE_SITES:
    COUNTRY_FOR_SEARCH = input("Job Country (i.e. USA): ")
    if COUNTRY_FOR_SEARCH == '':
        COUNTRY_FOR_SEARCH = 'USA'
else:
    COUNTRY_FOR_SEARCH = 'USA'

# Keywords to ignore in job titles (Max 20)
print("\nPlease give any keywords desired to filter out specific job titles")
print("Note capitalization does not matter -- Press ENTER when done:\n")
KEYWORDS_TO_IGNORE = []
for i in range(20):
    keyword = input(f"Job Title Keyword #{i+1}: ")
    if keyword == '':
        break
    elif len(keyword) < 2:
        print("Short keyword given (< 2 characters)! This can cut out many jobs, so it will be ignored.\n")
    else:
        KEYWORDS_TO_IGNORE.append(keyword)

# Only allow jobs with their minimum salary level above this amount
MIN_YEARLY_SALARY = ''
while MIN_YEARLY_SALARY == '':
    try:
        MIN_YEARLY_SALARY = int(input("\nMinimum Desired Yearly Salary: $"))
        if MIN_YEARLY_SALARY == '':
            raise ValueError()
    except:
        print("Please provide a valid salary!")
REQUIRE_SALARY_DATA = input("Require jobs to post salary ranges (This can remove many posts!)? (y/n): ").lower().__contains__('y')

# Determines if the extra columns below are dropped
DROP_EXTRA_COLUMNS = input("Remove columns with >67% N/A values (y is normal)? (y/n): ").lower().__contains__('y')

# Change the columns dropped before saving the CSV if the extra
# columns are set to be dropped. A lot of these tend to give no
# extra data which is why they are set to be dropped.
COLUMNS_TO_DROP = ['site', 'company_url', 'job_type', 'date_posted', 
                   'interval', 'num_urgent_words', 'benefits', 'emails', 
                   'description', 'currency', 'is_remote']

# Determines if a CSV of filtered results is saved to a csv
# SAVE_JOBS_CSV = input("Save results to a CSV after filtering? (y/n): ").lower().__contains__('y')
SAVE_JOBS_CSV = True # No reason for this to not be done

from jobspy import scrape_jobs
from webbrowser import open as open_page
from pandas import concat

# Warnings
if not SAVE_JOBS_CSV:
    correct = input("WARNING: Saving job results to CSV is OFF currently! Is this correct? (y/n): ")
    if correct.lower().__contains__('y'):
        print("Continuing with job scraping with NO CSV saving")
    else:
        SAVE_JOBS_CSV = True
        print("Save to CSV feature is now enabled!")

## Step 0 - Get job postings ##
print("\n#### STEP 0 - Getting initial job post data ####")
print("(Do note that this is the longest step!)\n")
# Get initial jobs
completed_first = False
for i, site in enumerate(USE_SITES):
    # Attempt using this single site for getting job results
    try:
        ## Job Spy ##
        ## Thx Bunsly ##
        new_jobs = scrape_jobs(
            site_name=[site],
            search_term=JOB_SEARCH_TITLE,
            location=JOB_SEARCH_LOCATION,
            results_wanted=NUM_RESULTS_PER_SITE,
            country_indeed=COUNTRY_FOR_SEARCH  # only needed for indeed / glassdoor
        )

        if not completed_first:
            jobs = new_jobs.copy()
            completed_first = True
            print(f"Currently gathered {len(jobs)} job posts")
        else:
            jobs = concat([new_jobs, jobs], ignore_index=True, sort=False)
            print(f"Currently gathered {len(jobs)} job posts")

    # If it fails (like with Indeed's 403 error), skip it
    except:
        continue
print()

# Verify Index
jobs.index = [*range(len(jobs))]

# Count and show some results
initial_num_jobs = len(jobs)
print(f"Got {len(jobs)} total job postings\n")


## Step 1 - Keywords filtering ##
print("\n#### STEP 1 - Drop jobs with keywords to ignore in their title ####\n")
for ind in jobs.index[::-1]:
    # For each job, run through keywords to see if they're in the job title
    for word in KEYWORDS_TO_IGNORE:
        # Remove the job if keyword is in job title
        if jobs['title'][ind].lower().__contains__(word.lower()):
            print(f"Dropped '{jobs['title'][ind]}', Contains Keyword '{word}'")
            jobs = jobs.drop(ind)
            break # Stop seaching through keywords if job was removed

# Final Results
dropped_indices = list(set([*range(initial_num_jobs)]).difference(set(jobs.index))) # lol sets are cool
dropped_indices.sort()
print(f"\nTotal Dropped Jobs: {len(dropped_indices)}")
print(f"Remaining Number of Jobs = {len(jobs)}\n")

# Check if any jobs left
if len(jobs) == 0:
    print()
    raise ValueError("No jobs left after filtering! Try expanding your search or reducing filters used\n")

# Reset jobs index
jobs.index = [*range(len(jobs))]



## Step 2 - Check minimum salary ##
min_hourly = MIN_YEARLY_SALARY / 2000
print("\n#### STEP 2 - Check that jobs' minimum salary is above the desired amount ####")
print("Given Salary Targets:")
print(f"Mimimum Yearly Salary: ${MIN_YEARLY_SALARY}/year")
print(f"Minimum Hourly Salary: ${min_hourly}/hr\n")

# This is slow but for under 100s of jobs its ok
for ind in jobs.index[::-1]:
    title = str(jobs['title'][ind])

    # Check that salary num is in USD, skip otherwise
    if type(jobs['currency'][ind]) == str:
        if jobs['currency'][ind].upper() != 'USD':
            print(f"Dropping '{title}', Currency is {jobs['currency'][ind]} not USD")
            jobs = jobs.drop(ind)
            dropped_indices.append(ind)
            continue

    elif REQUIRE_SALARY_DATA:
        if (jobs['currency'][ind] == None or \
            (type(jobs['min_amount'][ind]) == None and type(jobs['max_amount'][ind]) == None)) \
            and not title.__contains__('$'):
            # Drop NoneTypes
            print(f"Dropping '{title}' | Full Salary Data is Not Given")
            jobs = jobs.drop(ind)
            dropped_indices.append(ind)
            continue

    # Check job min salary
    salary_min = jobs['min_amount'][ind]
    salary_max = jobs['max_amount'][ind]

    # Edge case
    ## It's possible one value is None due to checks above
    ## Account for this instead of throwing a NoneType in min()
    if salary_max != None and salary_min != None:
        salary_true_min = min(salary_max, salary_min)
    elif salary_min == None:
        salary_true_min = salary_max
    elif salary_max == None:
        salary_true_min = salary_min

    # Second edge case
    ## Neither salary range found from scrape_jobs, but it is in the job title
    if salary_max == salary_min and salary_max == None and title.__contains__('$'):
        dollar_sign_index = title.index("$")
        salary_true_min = title[dollar_sign_index:dollar_sign_index+9] ## Should get approximately the whole value
        salary_true_min = [int(i) for i in salary_true_min if i.isdigit()]
        max_digits = len(str(MIN_YEARLY_SALARY))+1
        salary_true_min = salary_true_min[:max_digits]
        sal = ''
        for digit in salary_true_min:
            sal += str(digit)
        salary_true_min = int(sal)

        # Apply value to salary info since they aren't given
        ## This might not get the right min value, but it's in the title
        ## so at least the actual value will be seen during step 5
        jobs.loc[ind, ['min_amount', 'max_amount']] = salary_true_min


    # If given hourly, check if its above that min, drop otherwise
    try:
        if salary_true_min < 1000 and salary_true_min < min_hourly:
            print(f"Dropping '{title}' | Salary = ${salary_true_min}/hr < ${min_hourly}/hr")
            jobs = jobs.drop(ind)
            dropped_indices.append(ind)

        if salary_true_min > 1000 and salary_true_min < MIN_YEARLY_SALARY:
            print(f"Dropping '{title}' | Salary = ${salary_true_min}/Year < ${MIN_YEARLY_SALARY}/Year")
            jobs = jobs.drop(ind)
            dropped_indices.append(ind)

    # Note problem with program -- job should've been dropped or salary info fixed if here
    ## Quick fix should be to change REQUIRE_SALARY_DATA to True
    except:
        if REQUIRE_SALARY_DATA:
            print(f"Problem with salary information for '{title}' at '{jobs['company'][ind]}'")
        else:
            # Getting here is ok
            ## Having REQUIRE_SALARY_DATA be False means job roles with incomplete salary info
            ## can get through, meaning the above numerical comparisions couldn't be completed.
            ##
            ## Having REQUIRE_SALARY_DATA be True means a lot more jobs tend to get kicked out
            ## however. So, for more opportunities, have it be False is ok.
            pass

# Final Results
dropped_indices.sort()
print(f"\nTotal Dropped Jobs: {len(dropped_indices)}")
print(f"Remaining Number of Jobs = {len(jobs)}\n")

# Check if any jobs left
if len(jobs) == 0:
    print()
    raise ValueError("No jobs left after filtering! Try expanding your search or reducing filters used\n")

# Reset jobs index
jobs.index = [*range(len(jobs))]



## Step 3 - Verify Correct Locations ##
# For some reason this all needs to run multiple times for total completion
print("\n#### STEP 3 - Check the jobs' locations are given/correct ###\n")
for _ in range(3):
    for ind in jobs.index[::-1]:
        # Check job location
        location = jobs['location'][ind]
        if location in ['', 'United States', None]:
            print(f"Dropped '{jobs['title'][ind]}', Location is '{location}'")
            jobs = jobs.drop(ind)
            dropped_indices.append(ind)

    # Final Results
    dropped_indices.sort()

    # Check if any jobs left
    if len(jobs) == 0:
        print()
        raise ValueError("No jobs left after filtering! Try expanding your search or reducing filters used\n")

    # Reset jobs index
    jobs.index = [*range(len(jobs))]

print(f"\nTotal Dropped Jobs: {len(dropped_indices)}")
print(f"Remaining Number of Jobs = {len(jobs)}\n")



## Step 4 - Get rid of extra data ##
print("\n#### STEP 4 - Reduce the number of columns by removing (generally) not as useful ones ####\n")
# Drop some columns that are generally excess data with lots of NoneTypes or just not as useful data
all_columns = set(jobs.columns)

# Check number of unique entries in each col_to_drop
# if over 33% of postings have data, keep the column
for ci, cname in enumerate(COLUMNS_TO_DROP[::-1]):
    if jobs[cname].nunique() >= 0.33*len(jobs):
        COLUMNS_TO_DROP.pop(ci)

# Calculate remaining columns to keep
keep_columns = all_columns.difference(COLUMNS_TO_DROP)

# Keep this order for the base columns/info
first_cols = ['title', 'location', 'company', 'max_amount', 'min_amount', 'job_url']
keep_columns = keep_columns.difference(first_cols)
keep_columns = first_cols + list(keep_columns)

print(f"Removed {len(all_columns) - len(keep_columns)} Columns")
print(f"Names of columns removed: {COLUMNS_TO_DROP}\n")

# Set minimalized job columns
jobs = jobs[keep_columns]

# Save results
if SAVE_JOBS_CSV:
    jobs.to_csv("filtered_search.csv", index=False)
    print("Filtered results saved to filtered_search.csv")
    print(f"Results contain {len(jobs)} jobs postings\n")


## Step 5 - Run through jobs left and apply to them! ##
do_apps = input("\nContinue to Step 5 (Opening jobs to do applications)? [y/n]: ")
DO_APPLY_LOOP = do_apps.lower().__contains__('y')

if DO_APPLY_LOOP:
    print("#### STEP 5 - Apply to some jobs! ####\n")

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

            # Display next job after applying to current job
            if see_next.lower().__contains__('y'):
                print("Displaying next job ...\n")
                jobs = jobs.drop(ind)
                continue

            # Stop seeing jobs after applying to current one
            else:
                print("Okay, all done then!\n")
                jobs = jobs.drop(ind)
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

    # Finished
    if not finished_looking:
        print("No Jobs left to display!\n")

# Don't run through jobs to apply
else:
    print("Step 5 - Applications loop skipped!")
    print("(You can always use the secondary apply function later on the saved results)\n")