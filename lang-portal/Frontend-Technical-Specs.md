# Front Technical Specs

## Pages

### Dashboard `/dashboard`

#### Purpose
The purpose of the dashboard is to give the user a quick overview of their study progress and to provide a quick way to start studying.

#### Components

- Last Study Session
    - shows last activity used
    - shows when last activity was used
    - summarizes wrong vs correct from last activity
    - has a link to the group that was studied

- Study Progress
    - total words study eg. 3/125
        - accross all study sessions show the total number of words studied out of all possible words in our database
    - display a mastery progress bar eg. 25%

- Quick Stats
    - success rate eg. 63%
    - total study sessions eg. 5
    - total active groups eg. 3
    - study streak eg. 3 days

- Start Studying Button
    - goes to study activities page

#### Needed API Endpoints

GET /api/dashboard/last_study_session
GET /api/dashboard/study_progress
GET /api/dashboard/quick_stats

### Study Activities Index `/study_activities`

The purpose of the study activities page is to provide the user with a list of study activities they can do with a thumbnail and a description of the activity, to eather launch or view the study activity.

#### Components

- Study Activity Card
    - shows a thumbnail of the study activity
    - a name of the study activity
    - a launch button to take us to the launch page
    - the view page to view more information about past study sessions for this study activity

#### Needed API Endpoints

- GET /api/study_activities

### Study Activity Show `/study_activities/:id`

#### Purpose
The purpose of this page is to show the details of a study activity, including the past study sessions and the groups that were studied.

#### Components

- name of the study activity
- thumbnail of the study activity
- description of the study activity
- launch button to start the study activity
- study activities paginated list
    - id
    - activity name
    - group name
    - start time
    - end time (inferred by the last word_review_item submitted)
    - number of review items

#### Needed API Endpoints

- GET /api/study_activities/:id
- GET /api/study_activities/:id/study_sessions

### Study Activity Launch `/study_activities/:id/launch`

#### Purpose
The purpose of this page is to launch a study activity.

#### Components

- name of the study activity
- launch form
    - select field for group
    - launch now button

#### Behavior
After the form is submitted, a new tab opens with the study activity based on its URL provuded.

Also the after form is submitted the page will redirect to the study session show page.

#### Needed API Endpoints

- POST /api/study_activities


### Words index `/words`

#### Purpose
The purpose of the words page is to show all the words in the database.

#### Components
- pagenated list of words
    - Fields
        - spanish
        - transliteration
        - arabic
        - correct count
        - wrong count
    - pagination with 100 items per page
    - clicking the Spanish word will take us to the word show page

#### Needed API Endpoints
- GET /api/words

### Word Show `/words/:id`

#### Purpose
the purpose of the word show page is to show the details of a specific word. 

#### Components
- spanish
- transliteration
- arabic
- study statistics
    - correct count
    - wrong count
- word groups 
    - shown as a series of pills eg. tags
    - when group name is clicked it will take us to the group show page

#### Needed API Endpoints
- GET /api/words/:id

### Word Groups Index `/groups`

#### Purpose
the purpose of the word groups page is to show a list of groups in the database. 

#### Components
- pagenated group list
    - columns
        - group name
        - word count
    - clicking the group name will take us to the group show page

#### Needed API Endpoints
- GET /api/groups

### Group Show `/groups/:id`

#### Purpose
the purpose of the group show page is to show the details of a specific group.

#### Components
- group name
- group statistics
    - total words
- words in group (pagenated list of words)
    - should use the same component as the words index page
- study sessions (pagenated list of study sessions)
    - should use the same component as the study sessions index page

#### Needed API Endpoints
- GET /api/groups/:id (the name and group statistics)
- GET /api/groups/:id/words
- GET /api/groups/:id/study_sessions

### Study Sessions Index `/study_sessions`

#### Purpose
the purpose of the study sessions page is to show a list of study sessions in the database.

#### Components
- pagenated list of study sessions
    - columns
        - id
        - activity name
        - group name
        - start time
        - end time
        - number of review items
    - clicking the id will take us to the study session show page

#### Needed API Endpoints
- GET /api/study_sessions

### Study Session Show `/study_sessions/:id`

#### Purpose
the purpose of the study session show page is to show the details of a specific study session.

#### Components
- study session details
    - activity name
    - group name
    - start time
    - end time
    - number of review items
- word review items (pagenated list of word review items)
    - should be the same component as the word index page

#### Needed API Endpoints
- GET /api/study_sessions/:id
- GET /api/study_sessions/:id/words

### Settings Page `/settings`

#### Purpose
the purpose of the settings page is to allow the user to change their settings.

#### Components
- theme selector
    - light
    - dark
    - system
- reset history button
    - deletes all study sessions and word review items
- full reset button
    - this will drop all tables and reload the seed data

#### Needed API Endpoints
- POST /api/reset_history
- POST /api/full_reset

