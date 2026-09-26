default:
    @python main.py health

setup:
    @python main.py setup

test:
    @python main.py test

health:
    @python main.py health

clean:
    @python main.py clean

generate target=".":
    @python main.py generate --target {{target}}

audit target=".":
    @python main.py audit --target {{target}}
