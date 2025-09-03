#
# 2025/09/03 jinja2操作 POCコード(jinja2標準手順)
# jinja2のAPIドキュメントではEnvironmentとLoaderを使った方法が推奨されている
# https://jinja.palletsprojects.com/en/stable/api/#basics
# ただし、若干遅い
#
from jinja2 import Environment, DictLoader, BytecodeCache
import io
import datetime

jinja2_label_values = [
    "{{ A.chain_sum|int + 1 }}",
    "{{ B.zabbix_clock }}",
    "{{ A.type }}",
    "{{ B.zabbix_eventid }}",
    "{% if A.start_time %}{{ A.start_time }}{% else %}{{ B.zabbix_clock }}{% endif %}",
]
jinja2_label_values_dict = {
    jinja2_label_value: jinja2_label_value for jinja2_label_value in jinja2_label_values
}


class DictBytecodeCache(BytecodeCache):
    def __init__(self):
        self.cache_dict = {}

    def load_bytecode(self, bucket):
        cache = self.cache_dict.get(bucket.key)
        if cache is not None:
            bucket.load_bytecode(cache)

    def dump_bytecode(self, bucket):
        cache = io.BytesIO()
        bucket.write_bytecode(cache)
        self.cache_dict[bucket.key] = cache


LOOPS = 1000
JINJA2_CACHE = True

j2_cache = {}


def main():
    start = datetime.datetime.now()
    print(f"main start:{start}")
    env = Environment(
        loader=DictLoader(jinja2_label_values_dict), bytecode_cache=DictBytecodeCache()
    )
    for i in range(LOOPS):
        for jinja2_label_value in jinja2_label_values:
            if JINJA2_CACHE:
                template = env.get_template(jinja2_label_value)
            else:
                template = env.from_string(jinja2_label_value)

            label_value = template.render(
                A={"chain_sum": f"{i}", "type": "type-1"},
                B={
                    "zabbix_clock": f"2025/09/05 00:00:00.{i:04d}",
                    "zabbix_eventid": "event-{i:04d}",
                },
            )

    finish = datetime.datetime.now()
    print(f"main finish:{finish} ({finish - start})")
    print(f"label_value:{label_value}")


if __name__ == "__main__":
    main()
