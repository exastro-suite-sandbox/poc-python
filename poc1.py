#
# 2025/09/02 ディクショナリ操作 POCコード
#
import datetime

ZABBIX_EVENTS = 30_000
CONCLUSION_EVENTS = 1_000
UNUSED_EVENTS = 5

incident_dict = {}
labeled_events_dict = {}


def main():
    start = datetime.datetime.now()
    print(f'main start:{start}')
    setup_initial_data()
    get_unused_event()
    finish = datetime.datetime.now()
    print(f'main finish:{finish} ({finish - start})')


def get_unused_event():
    start = datetime.datetime.now()
    print(f'get_unused_event start:{start}')
    unused_event_ids = []

    # filter_match_list = {id: True for id_value_list in incident_dict.values() for id in id_value_list}
    filter_match_list = []
    for filter_id, id_value_list in incident_dict.items():
        if len(id_value_list) > 0:
            filter_match_list += id_value_list

    for event_id, event in labeled_events_dict.items():
        if event["labels"]["_exastro_evaluated"] != "0":
            continue
        if event_id not in filter_match_list:
            unused_event_ids.append(event_id)

    finish = datetime.datetime.now()
    print(f'get_unused_event finish:{finish} ({finish-start})')

    print(f"{len(filter_match_list)=}")
    print(f"{len(labeled_events_dict)=}")
    print(f"{len(unused_event_ids)=}")


def setup_initial_data():

    for i in range(ZABBIX_EVENTS):
        id1 = f"{i:06d}"
        exastro_evaluated = "1" if i < CONCLUSION_EVENTS else "0"

        labeled_events_dict[id1] = {
            "eventid": id1,
            "source": "0",
            "object": "0",
            "objectid": "16046",
            "clock": "",
            "ns": "906955445",
            "r_eventid": "0",
            "r_clock": "0",
            "r_ns": "0",
            "correlationid": "0",
            "userid": "0",
            "name": "High CPU utilization (over 90% for 5m)",
            "acknowledged": "0",
            "severity": "2",
            "opdata": "Current utilization: 100 %",
            "suppressed": "0",
            "urls": [],
            "labels": {
                "_exastro_evaluated": exastro_evaluated
            }
        }

        if i < ZABBIX_EVENTS - UNUSED_EVENTS:
            if 'fillter-1' not in incident_dict:
                incident_dict['fillter-1'] = [id1]
            else:
                incident_dict['fillter-1'].append(id1)

        if exastro_evaluated == '1':
            id2 = f"{i+ZABBIX_EVENTS:06d}"
            labeled_events_dict[id2] = {
                "eventid": id2,
                "labels": {
                    "_exastro_evaluated": "1"
                }
            }

            if 'fillter-2' not in incident_dict:
                incident_dict['fillter-2'] = [id2]
            else:
                incident_dict['fillter-2'].append(id2)


if __name__ == '__main__':
    main()