import random
import json


def _make_block(conditions, block_size, rng):
    """Return a shuffled list of conditions filling one block."""
    repeats = block_size // len(conditions)
    block = conditions * repeats
    rng.shuffle(block)
    return block


def assign_condition(db, config):
    """
    Return the next condition using permuted-block randomization.
    Block sizes are drawn randomly from config.BLOCK_SIZES.
    Mutates the randomization_state row in the database.
    """
    state = db.execute('SELECT * FROM randomization_state WHERE id = 1').fetchone()

    if state is None:
        seed = int(config.RNG_SEED) if config.RNG_SEED else None
        rng = random.Random(seed)
        block_size = rng.choice(config.BLOCK_SIZES)
        block = _make_block(config.CONDITIONS, block_size, rng)
        counts = {c: 0 for c in config.CONDITIONS}
        db.execute(
            'INSERT INTO randomization_state (id, current_block, condition_counts, rng_state) '
            'VALUES (1, ?, ?, ?)',
            (json.dumps(block), json.dumps(counts), json.dumps(rng.getstate()))
        )
        db.commit()
        state = db.execute('SELECT * FROM randomization_state WHERE id = 1').fetchone()

    block = json.loads(state['current_block'])
    counts = json.loads(state['condition_counts'])
    rng_state = json.loads(state['rng_state'])
    rng = random.Random()
    rng.setstate(tuple(
        tuple(x) if isinstance(x, list) else x for x in rng_state
    ))

    if not block:
        block_size = rng.choice(config.BLOCK_SIZES)
        block = _make_block(config.CONDITIONS, block_size, rng)

    condition = block.pop(0)
    counts[condition] += 1

    db.execute(
        'UPDATE randomization_state SET current_block = ?, condition_counts = ?, rng_state = ? WHERE id = 1',
        (json.dumps(block), json.dumps(counts), json.dumps(list(rng.getstate())))
    )
    db.commit()
    return condition
