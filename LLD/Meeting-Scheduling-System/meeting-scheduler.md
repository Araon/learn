## Design Meeting Scheduler
### Requirements
- There are n number of meeting rooms
- Book a meeting at any meeting room for a the given interval (start time, end time and capacity)
- Send notification to all the persons that is invited to the meeting
- Use meeting room calendar to track meetings date and time

now here the assumptions that i’ve taken
- There are n meeting room with different capacity
- We can book meeting room in the same day only
- Each user uses email to communicate
- We are not showing conflicts for each person. The person has to decide which meeting he/she wants to attend in case of two meeting booked at the same time

Now here are some of the classes that i’ve started with

class: Room, User, Meeting, Calender


