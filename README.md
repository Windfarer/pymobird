# pymobird
A python client for memobird printer

## Requirements
Python 3.4+

## Quick Example

```
from pymobird import Pymobird

bird = Pymobird(ak='your_memobird_ak')

user_id = bird.get_user_id(device_id='your_device_id_by_press_twice', user_identifying='some_name')
print(user_id)

content_id = bird.print_text(device_id, user_id, "hello pymobird!")
print(content_id)

# wait for a second, then
print(bird.check_printed(content_id))

```