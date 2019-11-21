
# https://www.meetup.com/{{HACKERSPACE_MEETUP_GROUP}}/
HACKERSPACE_MEETUP_GROUP = 'noisebridge'
EXTRA_MEETUP_GROUPS = ['Free-Code-Camp-SF', 'StartupSchool-SF']


EVENTS_SPACE_DEFAULT = 'Hackatorium'
EVENTS_SPACES_OVERWRITE = {
    'Whiteboarding & Algorithms Workshop': 'Church',
    'Noisebridge Python Class': 'Church',
    'Gamebridge Unityversity': 'Church',
    'Queer Game Developers Meetup': 'Church',
    'Laser Cutter Safety Training': 'SparkleForge',
}

# overwrite event hosts with their Discuss user names!
EVENTS_HOSTS_OVERWRITE = {
    # {{ STR: Name }}:{{ LIST: Hosts }}
    'Free Code Camp': ['tymeart'],
    'Noisebridge Sewing Project Night': ['tymeart'],
    'Laser Cutter Safety Training': ['ruthgrace'],
    'Noisebridge Extended Tour': ['pyconaut'],
    'Whiteboarding & Algorithms Workshop - Weekend Edition': ['Bernice'],
    'Circuit Hacking Mondays': ['spacegreens'],
    'BUIDL Night': ['kinnard'],
    'Startup School SF Meetup': ['kinnard'],
    'Gamebridge Unityversity C# Unity Game Dev - Art And Etcetera': ['Bernice', 'Mark'],
    'Gamebridge Unityversity Unity C# Game Development': ['Mark'],
    'Noisebridge Python Class': ['Jared'],
}

EVENTS_GUILDES_OVERWRITE = {
    # {{ STR: Keyword }}:{{ STR: Guilde Name }}
    'Laser': 'Laser Guilde',
    'Gamebridge': 'Gamebridge Guilde',
    'Electronics': 'Electronics Guilde',
    'Sewing': 'Sewing Guilde',
}
