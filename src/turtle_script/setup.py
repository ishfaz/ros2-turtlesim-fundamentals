from setuptools import find_packages, setup

package_name = 'turtle_script'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='tmkristi',
    maintainer_email='jonur@stud.ntnu.no',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'draw_circle = turtle_script.draw_circle:main', # Here frist the file name called draw_circle need name same as file name and then next second draw_circle is excutable can be of the diffeent name but here we keep it same name for sampilicity
            'area_service_server = turtle_script.area_service_server:main',
            'area_service_client = turtle_script.area_service_client:main',
            'Polygon_drawer = turtle_script.Polygon_drawer:main',
            'turtle_spawner = turtle_script.turtle_spawner:main',
            'turtle_controller = turtle_script.turtle_controller:main',
            'score_display = turtle_script.score_display:main'


        ],
    },
)
