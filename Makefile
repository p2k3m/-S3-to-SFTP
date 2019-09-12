install:
        mkdir -p dist
        python3.6 -m pip install --target ./dist -r requirements.txt

package: clean install
        cp main.py dist/
        cd dist; zip -r ../package.zip .

clean:
        rm -rf dist/
        rm -rf package.zip
