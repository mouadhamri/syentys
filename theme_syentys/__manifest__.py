{
    'name': 'Syentys Theme',
    'description': 'Clean and sharp design.',
    'category': 'Theme/Corporate',
    'summary': 'IT',
    'sequence': 110,
    'version': '15.0.0.0.0',
    'author': 'Syentys',
    'license': 'OPL-1',
    'website': 'https://syentys.com',
    'depends': ['website'],
    'data': [
        'data/ir_asset.xml',
        'views/images.xml',
        'views/customizations.xml',
        'views/home.xml',
        'views/footer.xml',
        'views/header.xml',
    ],
    'images': [
        'static/description/syentys_poster.jpg',
        'static/description/syentys_screenshot.jpg',
    ],
    'snippet_lists': {
        'homepage': ['s_cover', 's_image_text', 's_references', 's_three_columns', 's_comparisons', 's_call_to_action'],
    },
    'license': 'LGPL-3',
    'assets': {
        'website.assets_editor': [
            'theme_syentys/static/src/js/tour.js',
        ],
    }
}
