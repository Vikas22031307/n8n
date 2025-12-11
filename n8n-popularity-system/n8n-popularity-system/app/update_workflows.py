from .database import Base, engine, SessionLocal
from .crud import upsert_workflow
from .collectors.collect_youtube import collect_youtube_workflows
from .collectors.collect_forum import collect_forum_workflows
from .collectors.collect_trends import collect_trends_workflows
import sys, time

def run_update():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        print('[update] collecting YouTube...')
        yt = collect_youtube_workflows()
        print(f'[update] youtube items: {len(yt)}')

        print('[update] collecting Forum...')
        forum = collect_forum_workflows()
        print(f'[update] forum items: {len(forum)}')

        print('[update] collecting Trends...')
        trends = collect_trends_workflows()
        print(f'[update] trends items: {len(trends)}')

        all_items = yt + forum + trends
        print(f'[update] total items to upsert: {len(all_items)}')

        for i, item in enumerate(all_items):
            item['workflow'] = item.get('workflow', '').strip()
            item.setdefault('platform', 'Unknown')
            item.setdefault('country', 'US')
            upsert_workflow(db, item)
            if (i+1) % 50 == 0:
                print(f'[update] upserted {i+1}/{len(all_items)}')

        print('[update] done.')
    except Exception as e:
        print('[update] error:', e, file=sys.stderr)
    finally:
        db.close()

if __name__ == '__main__':
    run_update()
