{
   'name': 'Weather Notification Icon',
   'version': '19.0.1.0.0',
   'category': 'Tools',
   'summary': 'Systray Icon',
   'description': """Systray Icon fo weather notification  """,
   'depends': ['web'],
    'data': [
        'views/res_config_settings.xml',
    ],
   'assets': {
       'web.assets_backend': [
           'weather_notification/static/src/js/weather_notification.js',
           'weather_notification/static/src/xml/weather_notification.xml',
       ],
   },
   'application': True,
   'installable': True,
   'auto_install': True,
}
