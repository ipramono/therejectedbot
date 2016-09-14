from scheduler import Scheduler

sched = Scheduler().schedule
schedMsg = ""
for date in sched:
            for title in sched[date]:
                schedMsg += title + ": " + sched[date][title] + "\n"

print schedMsg