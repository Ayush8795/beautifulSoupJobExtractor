## Commands
To start the server run following commands one by one:

```shell
git clone https://github.com/Ayush8795/beautifulSoupJobExtractor.git

git switch new-branch

pip install -r requirements.txt

python app.py
```
click on the link generated the browser will open.

## Params
- `url`: The url from where the jobs are to be extracted.

- `topic`: The file name by which the extracted information has to be saved.

- `page_length`: number of webpages of the site that has to be parsed.

- `experience`: what target maximum experience is required.
This field is *optional*. If no value present -> **any** experience job is fetched.