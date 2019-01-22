# pymobird
A python client for memobird printer

[![PyPI version](https://badge.fury.io/py/pymobird.svg)](https://badge.fury.io/py/pymobird)

## Requirements
Python 3.4+
## Installation

```
pip install pymobird
```


## Quick Example

```python
from pymobird import SimplePymobird

# init client
bird = SimplePymobird(ak='your_memobird_ak', device_id='your_device_id_by_press_twice')


# print text
bird.print_text("hello pymobird!")


# print image
image_file_path = "./Hello.jpg"
bird.print_image(image_file)
# or
image_fp = open("./hello.jpg")
bird.print_image(image_fp)
image.close()

# print html by url
bird.print_url("http://example.com/a.html")

# print multi part content
from pymobird import Content
content = Content()
content.add_image(image_fp)
content.add_text("test text")
bird.print_multi_part_content(content)


# check content print status
content_id = bird.print_text("hello pymobird!")  # print and get content_id
# wait one second, then
is_printed = bird.check_printed(content_id)  
print(is_printed)

```
Besides, using ```Pymobird``` class directly for advanced usage. 
