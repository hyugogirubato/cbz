# CBZ-Helper
In order to be able to save digital books from images while saving metadata, this library will allow you to do it simply in python without having to go through a graphical client or external commands.

## Use
```python
import cbzhelper

if __name__ == '__main__':
    pages = [{'page_number': 0, 'content': b'', 'double_page': False}]
    helper = cbzhelper.Helper('eBook', 'Volume 1', replace=True)
    for page in pages:
        helper.addPage(page['page_number'], page['content'], double_page=page['double_page'])
    helper.addMetadata({
        'Title': 'Volume 1',
        'Series': 'Exemples',
        'Number': '1',
        'Volume': 1
    })
    helper.saveCBZ()

```

---
*This scripts are created by __hyugogirubato__.  
Find us on [discord](https://discord.com/invite/g6JzYbh) for more information on projects in development.*
