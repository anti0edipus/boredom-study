import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-before-deploying-abc123')
    DATABASE_PATH = os.environ.get('DATABASE_PATH', '/data/study.db')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'changeme')
    PROLIFIC_COMPLETION_URL = os.environ.get(
        'PROLIFIC_COMPLETION_URL',
        'https://app.prolific.co/submissions/complete?cc=PLACEHOLDER'
    )
    RNG_SEED = os.environ.get('RNG_SEED', None)
    MIN_WRITING_TIME_SEC = int(os.environ.get('MIN_WRITING_TIME_SEC', '180'))
    MIN_WRITING_CHARS = int(os.environ.get('MIN_WRITING_CHARS', '400'))
    BORING_TASK_DURATION_SEC = int(os.environ.get('BORING_TASK_DURATION_SEC', '300'))
    BORING_TASK_TARGET = os.environ.get('BORING_TASK_TARGET', 'X')
    FORCE_DESKTOP = os.environ.get('FORCE_DESKTOP', 'true').lower() == 'true'
    CONDITIONS = ['meaning', 'autonomy', 'control']
    BLOCK_SIZES = [3, 6, 9]
