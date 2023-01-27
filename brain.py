from random import randint


L = 100
FIELDS = {}

BOXES = []
OPENED_BOXES = []
DELETED_BOXES = []
PLAYERS = {}
COUNT_PLAYERS = 0


def start(L: int = 100, COUNT_PLAYERS: int = 0) -> list:
    result = []
    return result


def main(event: tuple, BOXES: list, OPENED_BOXES: list, DELETED_BOXES: list) -> list:
    result = []
    for ev in event:
        print(ev)
        if ev == 'make_field':
            result.append(make_fields())
        elif ev == '':
            pass
        elif ev == '':
            pass
    return result


def game() -> None:
    lets_sleep, running_game = False, True
    while running_game:
        if lets_sleep:
            lets_sleep = False
            OPENED_BOXES.clear()

        if len(DELETED_BOXES) == len(BOXES):
            running_game = False
            if box[1] in DELETED_BOXES:
                continue
            OPENED_BOXES.append(box)

            if len(OPENED_BOXES) == 2:
                if FIELDS[f'{OPENED_BOXES[0][1]}'] == FIELDS[f'{OPENED_BOXES[1][1]}']:
                    PLAYERS[f'{I % COUNT_PLAYERS}'][0] += 1
                    DELETED_BOXES.append(OPENED_BOXES[0][1]), DELETED_BOXES.append(OPENED_BOXES[1][1])
                    lets_sleep = True


def make_fields() -> dict:
    global FIELDS, DELETED_BOXES, OPENED_BOXES

    for i in range(L // 2):
        rnd = randint(0, 9)
        FIELDS[str(L // 2 + i)] = rnd
        FIELDS[str(i)] = rnd
    OPENED_BOXES.clear(), DELETED_BOXES.clear()
    return FIELDS
