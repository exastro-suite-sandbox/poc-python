#
# 2025/09/02 jinja2操作 POCコード
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
JINJA2_CACHE = True

j2_cache = {}


def main():
    start = datetime.datetime.now()
    print(f'main start:{start}')
    for i in range(LOOPS):
        for jinja2_label_value in jinja2_label_values:
            if JINJA2_CACHE:
                if jinja2_label_value in j2_cache:
                    template = j2_cache[jinja2_label_value]
                else:
                    template = Template(jinja2_label_value)
                    j2_cache[jinja2_label_value] = template
            else:
                template = Template(jinja2_label_value)

            label_value = template.render(
                A={"chain_sum": f"{i}", "type": "type-1"},
                B={"zabbix_clock": f"2025/09/05 00:00:00.{i:04d}", "zabbix_eventid": "event-{i:04d}"})

    finish = datetime.datetime.now()
    print(f'main finish:{finish} ({finish - start})')
    print(f"label_value:{label_value}")


if __name__ == '__main__':
    main()