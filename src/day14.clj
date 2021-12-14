(ns day14
  (:require
   [clojure.string :as str]
   [clojure.test :as t]))

(def example-in (str/split-lines "NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"))

(defn get-polymer-template
  [lines]
  (zipmap (partition 2 1 (first lines)) (repeat 1)))

(defn get-insertion-rules
  [lines]
  (->> lines
       (drop 2)
       (map #(str/split %1 #" -> "))
       (map (fn [ln] (vector (seq (first ln)) (first (seq (second ln))))))
       (into {})))

(defn submarine-incrementer
  [b]
  (fn [a]
    (if (nil? a)
      b
      (+ a b))))

(defn add-new-pairs
  {:test #(t/is
           (= {'(\N \C) 1, '(\C \N) 1}
              (add-new-pairs {'(\N \N) \C, '(\N \C) \B, '(\C \B) \H} {}  '(\N \N) 1)))}
  [rules polymer pair reps]
  (let [to-inject (rules pair)]
    (-> polymer
        (update ,,, [(first pair) to-inject] (submarine-incrementer reps))
        (update ,,, [to-inject (second pair)] (submarine-incrementer reps)))))

(defn do-step
  {:test #(t/is
           (= {'(\N \C) 1, '(\C \N) 1 '(\N \B) 1 '(\B \C) 1 '(\C \H) 1 '(\H \B) 1}
              (do-step {'(\N \N) 1, '(\N \C) 1, '(\C \B) 1} {'(\N \N) \C, '(\N \C) \B, '(\C \B) \H})))}
  [polymer rules]
  (reduce-kv (partial add-new-pairs rules) {} polymer))

(defn do-steps
  [polymer rules steps]
  (loop [n steps p polymer]
    (if (zero? n)
      p
      (recur (dec n) (do-step p rules)))))

(defn get-frequencies
  {:test #(t/is
           (= {\N 2 \C 1 \B 1}
              (get-frequencies {'(\N \N) 1, '(\N \C) 1, '(\C \B) 1})))}
  [polymer]
  (->> polymer
       (reduce-kv
        (fn [counts pair pair-count]
          (-> counts
              (update ,,, (first pair) (submarine-incrementer pair-count))
              (update ,,, (second pair) (submarine-incrementer pair-count))))
        {})
       (map (fn [[k v]] {k (if (even? v) (/ v 2) (/ (inc v) 2))}))
       (into {})))

(defn solve
  {:test #(t/is (= 1588 (solve example-in 10)))}
  [lines steps]
  (let [polymer-template (get-polymer-template lines)
        rules (get-insertion-rules lines)
        result (do-steps polymer-template rules steps)
        fq (get-frequencies result)
        biggest (reduce max (vals fq))
        smallest (reduce min (vals fq))]
    (- biggest smallest)))

(t/run-tests)
