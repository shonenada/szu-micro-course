from setuptools import setup, find_packages


install_required = [l.strip() for l in open("requirements.txt", "r")]


metadata = {'name': 'szu-mooc',
            'version': '0.1',
            'packages': find_packages(),
            'author': 'shonenada @ League of Tech Team',
            'author_email': 'shonenada@gmail.com',
            'url': "https://github.com/league-of-tech/mooc",
            'zip_safe': False,
            'platforms': ['linux'],
            'package_data': {"": ['*.html', '*.jpg', '*.png', '*.css', '*.js',
                                  '*.ico', '*.coffee', '*.less', '*.stylus']},
            'install_requires': install_required,
            'description': 'A MOOC system for SZU.'}


if __name__ == '__main__':
    setup(**metadata)
