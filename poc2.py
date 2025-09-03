#
# 2025/09/02 jinja2操作 POCコード()
#
from jinja2 import Template
import datetime

jinja2_label_values = [
    "{{ A.chain_sum|int + 1 }}",
    "{{ B.zabbix_clock }}",
    "{{ A.type }}",
    "{{ B.zabbix_eventid }}",
    "{% if A.start_time %}{{ A.start_time }}{% else %}{{ B.zabbix_clock }}{% endif %}"
]

LOOPS = 1000


def main():
    start = datetime.datetime.now()
    print(f'main start:{start}')
    for i in range(LOOPS):
        for jinja2_label_value in jinja2_label_values:
            template = Template(jinja2_label_value)
            label_value = template.render(
                A={"chain_sum": "1", "type": "type-1"},
                B={"zabbix_clock": "2025/09/05", "zabbix_eventid": "event-1"})

    finish = datetime.datetime.now()
    print(f'main finish:{finish}')
    print(f"label_value:{label_value}")


if __name__ == '__main__':
    main()