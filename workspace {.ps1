workspace {
    model {
        user = person "User" "Represents all users including students, freshers, and job seekers."
        recruiter = person "Recruiter" "Posts jobs and searches for candidates."
        
        system = softwareSystem "Skill Validation and Job Matching System" "Helps users validate skills, recommend jobs, and find gaps."

        externalUdemy = softwareSystem "Udemy API" "Provides certification validation."
        externalCoursera = softwareSystem "Coursera API" "Provides certification validation."
        externalLinkedIn = softwareSystem "LinkedIn API" "Fetches job postings and profile data."

        user -> system "Uses to validate skills and find job recommendations"
        recruiter -> system "Uses to find suitable candidates"
        system -> externalUdemy "Validates certifications"
        system -> externalCoursera "Validates certifications"
        system -> externalLinkedIn "Fetches job postings and profiles"
    }

    views {
        systemContext system {
            include *
            autolayout lr
        }

        styles {
            element "Person" {
                shape person
                background #84bbf0
                color #000000
            }
            element "Software System" {
                shape roundedBox
                background #cccccc
                color #000000
            }
        }
    }
}