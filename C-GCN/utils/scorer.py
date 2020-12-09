#!/usr/bin/env python

"""
Score the predictions with gold labels, using precision, recall and F1 metrics.
"""

import argparse
import sys
from collections import Counter
from utils.category_maps import category_maps

NO_RELATION = "no_relation"

def parse_arguments():
    parser = argparse.ArgumentParser(description='Score a prediction file using the gold labels.')
    parser.add_argument('gold_file', help='The gold relation file; one relation per line')
    parser.add_argument('pred_file',
                        help='A prediction file; one relation per line, in the same order as the gold file.')
    args = parser.parse_args()
    return args


def score(key, prediction, verbose=False):
    correct_by_relation = Counter()
    guessed_by_relation = Counter()
    gold_by_relation = Counter()
    misclassified_indices = []
    correct_indices = []
    wrong_predictions = []
    # Loop over the data to compute a score
    for row in range(len(key)):
        gold = key[row]
        guess = prediction[row]

        if gold == NO_RELATION and guess == NO_RELATION:
            pass
        elif gold == NO_RELATION and guess != NO_RELATION:
            guessed_by_relation[guess] += 1
        elif gold != NO_RELATION and guess == NO_RELATION:
            gold_by_relation[gold] += 1
        elif gold != NO_RELATION and guess != NO_RELATION:
            guessed_by_relation[guess] += 1
            gold_by_relation[gold] += 1
            if gold == guess:
                correct_by_relation[guess] += 1
        if gold == guess:
            correct_indices.append(row)
        else:
            misclassified_indices.append(row)
            wrong_predictions.append(guess)

    # Print verbose information
    if verbose:
        print("Per-relation statistics:")
        relations = gold_by_relation.keys()
        longest_relation = 0
        for relation in sorted(relations):
            longest_relation = max(len(relation), longest_relation)
        for relation in sorted(relations):
            # (compute the score)
            correct = correct_by_relation[relation]
            guessed = guessed_by_relation[relation]
            gold = gold_by_relation[relation]
            prec = 1.0
            if guessed > 0:
                prec = float(correct) / float(guessed)
            recall = 0.0
            if gold > 0:
                recall = float(correct) / float(gold)
            f1 = 0.0
            if prec + recall > 0:
                f1 = 2.0 * prec * recall / (prec + recall)
            # (print the score)
            sys.stdout.write(("{:<" + str(longest_relation) + "}").format(relation))
            sys.stdout.write("  P: ")
            if prec < 0.1: sys.stdout.write(' ')
            if prec < 1.0: sys.stdout.write(' ')
            sys.stdout.write("{:.2%}".format(prec))
            sys.stdout.write("  R: ")
            if recall < 0.1: sys.stdout.write(' ')
            if recall < 1.0: sys.stdout.write(' ')
            sys.stdout.write("{:.2%}".format(recall))
            sys.stdout.write("  F1: ")
            if f1 < 0.1: sys.stdout.write(' ')
            if f1 < 1.0: sys.stdout.write(' ')
            sys.stdout.write("{:.2%}".format(f1))
            sys.stdout.write("  #: %d" % gold)
            sys.stdout.write("\n")
        print("")

    if verbose:
        print('Per-category statistics:')
        relations = gold_by_relation.keys()
        longest_relation = 0
        for relation in sorted(relations):
            longest_relation = max(len(relation), longest_relation)
        category2records = {}
        for category in category_maps:
            category2records[category] = {'correct_by_relation': [], 'guessed_by_relation': [], 'gold_by_relation': []}
        for relation in relations:
            for category, category_relations in category_maps.items():
                if relation in category_relations:
                    correct = correct_by_relation[relation]
                    guessed = guessed_by_relation[relation]
                    gold = gold_by_relation[relation]
                    category2records[category]['correct_by_relation'].append(correct)
                    category2records[category]['guessed_by_relation'].append(guessed)
                    category2records[category]['gold_by_relation'].append(gold)
        category_f1s = {}
        for category, records in category2records.items():
            correct_by_category = sum(records['correct_by_relation'])
            guessed_by_category = sum(records['guessed_by_relation'])
            gold_by_category = sum(records['gold_by_relation'])

            tp = correct_by_category
            fp = guessed_by_category - correct_by_category
            fn = gold_by_category - correct_by_category

            precision = 1.0
            if guessed_by_category > 0:
                precision = float(correct_by_category) / float(guessed_by_category)
            recall = 0
            if gold_by_category > 0:
                recall = float(correct_by_category) / float(gold_by_category)
            f1 = 0
            if precision + recall > 0:
                f1 = 2.0 * precision * recall / (precision + recall)

            category_f1s[category] = f1

            sys.stdout.write(("{:<" + str(longest_relation) + "}").format(category))
            sys.stdout.write("  P: ")
            if precision < 0.1: sys.stdout.write(' ')
            if precision < 1.0: sys.stdout.write(' ')
            sys.stdout.write("{:.2%}".format(precision))
            sys.stdout.write("  R: ")
            if recall < 0.1: sys.stdout.write(' ')
            if recall < 1.0: sys.stdout.write(' ')
            sys.stdout.write("{:.2%}".format(recall))
            sys.stdout.write("  F1: ")
            if f1 < 0.1: sys.stdout.write(' ')
            if f1 < 1.0: sys.stdout.write(' ')
            sys.stdout.write("{:.2%}".format(f1))
            sys.stdout.write("  #: %d" % gold_by_category)
            sys.stdout.write("  TP: %d" % tp)
            sys.stdout.write("  FP: %d" % fp)
            sys.stdout.write("  FN: %d" % fn)
            sys.stdout.write("\n")

    # Print the aggregate score
    if verbose:
        print("Final Score:")
    prec_micro = 1.0
    if sum(guessed_by_relation.values()) > 0:
        prec_micro = float(sum(correct_by_relation.values())) / float(sum(guessed_by_relation.values()))
    recall_micro = 0.0
    if sum(gold_by_relation.values()) > 0:
        recall_micro = float(sum(correct_by_relation.values())) / float(sum(gold_by_relation.values()))
    f1_micro = 0.0
    if prec_micro + recall_micro > 0.0:
        f1_micro = 2.0 * prec_micro * recall_micro / (prec_micro + recall_micro)
    print("Precision (micro): {:.3%}".format(prec_micro))
    print("   Recall (micro): {:.3%}".format(recall_micro))
    print("       F1 (micro): {:.3%}".format(f1_micro))
    return {'f1': f1_micro, 'precision': prec_micro, 'recall': recall_micro}, \
           {'wrong_indices': misclassified_indices, 'correct_indices': correct_indices,
            'wrong_predictions': wrong_predictions}


if __name__ == "__main__":
    # Parse the arguments from stdin
    args = parse_arguments()
    key = [str(line).rstrip('\n') for line in open(str(args.gold_file))]
    prediction = [str(line).rstrip('\n') for line in open(str(args.pred_file))]

    # Check that the lengths match
    if len(prediction) != len(key):
        print("Gold and prediction file must have same number of elements: %d in gold vs %d in prediction" % (
        len(key), len(prediction)))
        exit(1)

    # Score the predictions
    score(key, prediction, verbose=True)