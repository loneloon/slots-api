import numpy as np
import copy
import uuid
import hashlib
import datetime

from models.reel import Reel


class Screen:
    def __init__(self, reels, min_matches_for_cluster, payout_ratio):
        self.reels = np.array(reels)
        self.array_width = self.reels.shape[0]
        self.array_height = self.reels.shape[1]

        self.min_matches_for_cluster = min_matches_for_cluster
        self.payout_ratio = payout_ratio

        # Marking evaluated cells with nulls
        self.matrix_memory = copy.deepcopy(self.reels)
        self.clusters = self.find_combinations()

    def __repr__(self):
        return str(self.reels)

    def find_combinations(self):

        combinations = []

        for row_idx in range(self.array_height):
            for col_idx in range(self.array_width):

                if self.matrix_memory[row_idx, col_idx] is not None:
                    current_combination = self.build_chain(row_idx, col_idx, True)

                    if current_combination and len(current_combination) >= self.min_matches_for_cluster:
                        combinations.append(current_combination)
        return combinations

    # Depth first search algorithm
    def build_chain(self, row_idx, col_idx, isFirstElement):
        current_cell = self.reels[row_idx, col_idx]
        chain = []

        didMatch = False

        if isFirstElement:
            self.matrix_memory[row_idx, col_idx] = None

        #  Checking right connection
        if col_idx + 1 <= self.array_width - 1 and self.matrix_memory[row_idx, col_idx + 1] is not None:
            next_right_cell = self.reels[row_idx, col_idx + 1]

            if current_cell.key == next_right_cell.key:
                didMatch = True
                self.matrix_memory[row_idx, col_idx + 1] = None
                chain.extend(self.build_chain(row_idx, col_idx + 1, False))

        # Checking bottom connection
        if row_idx + 1 <= self.array_height - 1 and self.matrix_memory[row_idx + 1, col_idx] is not None:
            next_bottom_cell = self.reels[row_idx + 1, col_idx]

            if current_cell.key == next_bottom_cell.key:
                didMatch = True
                self.matrix_memory[row_idx + 1, col_idx] = None
                chain.extend(self.build_chain(row_idx + 1, col_idx, False))

        # Checking left connection
        if col_idx - 1 >= 0 and self.matrix_memory[row_idx, col_idx - 1] is not None:
            next_left_cell = self.reels[row_idx, col_idx - 1]

            if current_cell.key == next_left_cell.key:
                didMatch = True
                self.matrix_memory[row_idx, col_idx - 1] = None
                chain.extend(self.build_chain(row_idx, col_idx - 1, False))

        # Checking top connection
        if row_idx - 1 >= 0 and self.matrix_memory[row_idx - 1, col_idx] is not None:
            next_top_cell = self.reels[row_idx - 1, col_idx]

            if current_cell.key == next_top_cell.key:
                didMatch = True
                self.matrix_memory[row_idx - 1, col_idx] = None
                chain.extend(self.build_chain(row_idx - 1, col_idx, False))

        # If is first element and there are connections delete from matrix and add self to start
        if isFirstElement and didMatch:
            chain.insert(0, [current_cell, [row_idx, col_idx]])

        # If not the first element (already matched with  someone previously) delete from matrix and add self to start
        if not isFirstElement:
            self.matrix_memory[row_idx, col_idx] = None
            chain.insert(0, [current_cell, [row_idx, col_idx]])

        return chain

    def stringify_matrix(self):
        # try to validate this
        return {f'{i}{j}':self.reels[j, i].key for i in range(self.array_width) for j in range(self.array_height)}

    def calculate_payout_modifier(self, streak, symbol_value):
        return self.payout_ratio * streak * ((symbol_value+1)**2)

    def generate_single_cluster_dto(self, cluster):
        cluster_coordinates_stringified = ':'.join([str(cell[1][1]) + str(cell[1][0]) for cell in cluster])
        accumulated_points = self.calculate_payout_modifier(len(cluster), cluster[0][0].value)
        cluster_id = str(uuid.uuid4())
        created_at = datetime.datetime.now()
        secret = cluster_coordinates_stringified + str(accumulated_points) + str(created_at)

        dto = {
            'coordinates': cluster_coordinates_stringified,
            'payout_modifier': accumulated_points,
            'id': cluster_id,
            'datetime': str(created_at),
            'signature': hashlib.md5(secret.encode('UTF-8')).hexdigest()
        }

        self.persist_single_cluster_record(dto)
        return dto

    def persist_single_cluster_record(self, cluster_dto):
        print("Warning! Database was not enabled for this application. Cluster persistence will not be recorded!")

    def generate_clusters_dto(self, clusters):
        return [self.generate_single_cluster_dto(cluster) for cluster in clusters]

    def generate_response_dto(self):
        return {
            'matrix': self.stringify_matrix(),
            'matches': bool(self.clusters),
            'clusters': self.generate_clusters_dto(self.clusters)
        }


class ScreenFactory:
    @staticmethod
    def build(width, height, min_matches_for_cluster, payout_ratio):
        return Screen(list(Reel(height).keys for r in range(width)), min_matches_for_cluster, payout_ratio)
