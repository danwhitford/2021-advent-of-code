(ns day6
  (:require
   [clojure.string :as str]
   [clojure.test :as t]))

(def example-in (str/split-lines "3,4,3,1,2"))

(defn line-to-gen
  [line]
  {:test #(t/is (= {2 2 3 1 0 1 1 1} (line-to-gen "2,3,2,0,1")))}
  (->> (map #(Integer/parseInt %1) (str/split line #",")) (frequencies)))

(defn next-gen
  {:test #(t/is (= {0 1, 7 0, 1 2, 4 0, 6 1, 3 0, 2 1, 5 0, 8 1} (next-gen {2 2 3 1 0 1 1 1})))}
  [gen]
  (hash-map
   0 (get gen 1 0)
   1 (get gen 2 0)
   2 (get gen 3 0)
   3 (get gen 4 0)
   4 (get gen 5 0)
   5 (get gen 6 0)
   6 (+ (get gen 7 0) (get gen 0 0))
   7 (get gen 8 0)
   8 (get gen 0 0)))

(defn solve
  {:test #(t/testing
           (t/is (= 26 (solve example-in 18)))
            (t/is (= 5934 (solve example-in 80)))
            (t/is (= 26984457539 (solve example-in 256))))}
  [lines days]
  (let [starting-gen (line-to-gen (first lines))]
    (loop [gen starting-gen cnt days]
      (if (= 0 cnt)
        (apply + (vals gen))
        (recur (next-gen gen) (dec cnt))))))

(t/run-tests)
