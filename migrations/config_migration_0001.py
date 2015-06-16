import logging
import sqlite3

migrate_forward = """
    UPDATE
        scenarios
    SET
        expression = REPLACE(expression,
            '"type":"RequestNode"',
            '"type":"RequestNode", "referenceProcessing": "substitute"'
        )
"""

migrate_back = """
    UPDATE
        scenarios
    SET
        expression = REPLACE(expression,
            '"type":"RequestNode", "referenceProcessing": "substitute"',
            '"type":"RequestNode"'
        )
"""

migration_script = migrate_forward

logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] [%(asctime)s] (%(threadName)-10s) %(message)s',
                    filename='debug.log', filemode='a')

with sqlite3.connect('../config.db') as conn:
    cur = conn.cursor()
    cur.execute(migration_script)
    conn.commit()
    logging.info('Migration complete successfully. Script: '+migration_script)


