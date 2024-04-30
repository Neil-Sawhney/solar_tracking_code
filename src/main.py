import helpers.gpio as gpio
from modules.actuation import follow_plan
from modules.planner import get_daily_plan


def main():
    while True:
        # home the actuator
        print("Homing actuator")
        gpio.expand_actuator(10e3)

        print("Getting daily plan")
        daily_plan = get_daily_plan()

        print("Following daily plan")
        print(daily_plan)
        follow_plan(daily_plan)


if __name__ == "__main__":
    main()
