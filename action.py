# Copyright 2024 NEC Corporation#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from jinja2 import Template


def getIDtoLabelName(label_master: dict[str], uuid):
    uuid = str(uuid)
    if uuid not in label_master:
        return False
    return label_master[uuid]


class ManageEvents:
    """ManageEventsのmock"""
    
    def __init__(self, labeled_events_dict: dict[bytes, dict[str]] | None = None):
        self.labeled_events_dict = {"labels": {}} if labeled_events_dict is None else labeled_events_dict


    def get_events(self, event_id: bytes):
        if event_id not in self.labeled_events_dict:
            return False, {}
        return True, self.labeled_events_dict[event_id]


class Action:
    def __init__(self, EventObj: ManageEvents):
        self.EventObj = EventObj

    def generateConclusionLables(
        self,
        UseEventIdList: list[bytes],
        ruleRow: dict[str, list[dict]],
        labelMaster: dict[str, str],
        action_label_inheritance_flg: str,
        event_label_inheritance_flg: str,
    ):
        # アクションに利用 & 結論イベントに付与 するラベルを生成する
        action_parameters = {}
        conclusion_event_lables = {"labels": {}, "exastro_label_key_inputs": {}}

        ab_merged_labels = {}  # 元イベントのラベルを継承するラベル
        setting_only_labels = {}  # 結論ラベル設定のみのラベル

        # フィルターA, Bそれぞれに対応するイベント取得
        ret_bool_A, event_A = self.EventObj.get_events(UseEventIdList[0])
        if len(UseEventIdList) == 2:
            ret_bool_B, event_B = self.EventObj.get_events(UseEventIdList[1])
        else:
            event_B = {"labels": {}}

        # labelsのマージ
        event_A_labels = event_A["labels"]
        event_B_labels = event_B["labels"]

        if action_label_inheritance_flg == "1" or event_label_inheritance_flg == "1":
            ab_merged_labels = event_B_labels

            # システム用のラベルは除外
            key_name_to_exclude = [
                "_exastro_event_collection_settings_id",
                "_exastro_fetched_time",
                "_exastro_end_time",
                "_exastro_evaluated",
                "_exastro_undetected",
                "_exastro_timeout",
                "_exastro_checked",
                "_exastro_type",
                "_exastro_rule_name",
            ]
            # フィルターAに該当するイベントのラベルを優先して上書き
            for label_key_name in event_A_labels:
                if label_key_name not in key_name_to_exclude:
                    ab_merged_labels[label_key_name] = event_A_labels[label_key_name]

        # 結論ラベル設定で上書き
        conc_label_settings = ruleRow["CONCLUSION_LABEL_SETTINGS"]  # LIST
        for setting in conc_label_settings:
            # label_key_idをlabel_key_nameに変換
            label_key_name = getIDtoLabelName(labelMaster, setting["label_key"])
            # label_valueに変数ブロックが含まれている場合、jinja2テンプレートで値を変換
            template: Template = Template(setting["label_value"])
            try:
                label_value = template.render(A=event_A_labels, B=event_B_labels)
            except Exception as e:
                # POC上では不要処理のためコメントアウト
                # t = traceback.format_exc()
                # g.applogger.info("[timestamp={}] {}".format(str(get_iso_datetime()), arrange_stacktrace_format(t)))

                label_value = "CONCLUSION LABELS jinja2TEMPLATE ERROR ({})".format(e)

            ab_merged_labels[label_key_name] = label_value
            setting_only_labels[label_key_name] = label_value

        # アクションパラメータに使うラベル
        if action_label_inheritance_flg == "1":
            action_parameters = ab_merged_labels
        else:
            action_parameters = setting_only_labels
        # 結論イベントにつけるラベル
        if event_label_inheritance_flg == "1":
            conclusion_event_lables["labels"] = ab_merged_labels
        else:
            conclusion_event_lables["labels"] = setting_only_labels

        # 　exastro_label_key_inputs
        if event_label_inheritance_flg == "0":
            for label_key_name in setting_only_labels:
                for master_label_id, master_label_key_name in labelMaster.items():
                    if label_key_name == master_label_key_name:
                        conclusion_event_lables["exastro_label_key_inputs"][
                            label_key_name
                        ] = master_label_id
        else:
            for label_key_name in ab_merged_labels:
                for master_label_id, master_label_key_name in labelMaster.items():
                    if label_key_name == master_label_key_name:
                        conclusion_event_lables["exastro_label_key_inputs"][
                            label_key_name
                        ] = master_label_id

        return action_parameters, conclusion_event_lables
