# Copyright 2023 NEC Corporation#
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

from itertools import chain


class ManageEvents:
    def __init__(self, labeled_events_dict: dict[bytes, dict[str, dict[str, str]]] | None = None):
        # self.labeled_event_collection = wsMongo.collection(mongoConst.LABELED_EVENT_COLLECTION)
        # # 以下条件のイベントを取得
        # undetermined_search_value = {
        #     "labels._exastro_timeout": "0",
        #     "labels._exastro_evaluated": "0",
        #     "labels._exastro_undetected": "0"
        # }
        # labeled_events = self.labeled_event_collection.find(undetermined_search_value)

        self.labeled_events_dict: dict[bytes, dict[str, dict[str, str]]] = (
            labeled_events_dict if labeled_events_dict is not None else {}
        )

        # for event in labeled_events:
        #     event[oaseConst.DF_LOCAL_LABLE_NAME] = {}
        #     event[oaseConst.DF_LOCAL_LABLE_NAME]["status"] = None

        #     check_result, event_status = self.check_event_status(
        #         int(judgeTime),
        #         int(event["labels"]["_exastro_fetched_time"]),
        #         int(event["labels"]["_exastro_end_time"]),
        #     )
        #     if check_result is False:
        #         continue

        #     self.add_local_label(
        #         event,
        #         oaseConst.DF_LOCAL_LABLE_NAME,
        #         oaseConst.DF_LOCAL_LABLE_STATUS,
        #         event_status
        #     )
        #     self.labeled_events_dict[event["_id"]] = event

    def get_unused_event(self, incident_dict: dict[bytes, list[bytes]]):
        """
        フィルタにマッチしていないイベントを抽出

        Arguments:
            incident_dict: メモリーに保持している、フィルターID:（マッチした）イベント（id or id-list）、形式のリスト
            filterIDMap:
        Returns:
            unused_event_ids(dict)
        """
        unused_event_ids: list[bytes] = []

        # incident_dictに登録されているイベントをfilter_match_listに格納する
        filter_match_list: frozenset[bytes] = frozenset(
            chain.from_iterable(incident_dict.values())
        )

        for event_id, event in self.labeled_events_dict.items():
            # タイムアウトしたイベントは登録されているのでスキップ
            if event["labels"]["_exastro_timeout"] != "0":
                continue
            # ルールにマッチしているイベント
            if event["labels"]["_exastro_evaluated"] != "0":
                continue

            # keyが削除されてincident_dictが空になっている場合（or条件で両方のフィルターにマッチしていた場合）があるのでここで判定する
            if len(incident_dict) == 0:
                unused_event_ids.append(event_id)
                continue

            # フィルターにマッチしなかった
            if event_id not in filter_match_list:
                unused_event_ids.append(event_id)

        return unused_event_ids
