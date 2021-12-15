(ns day15
  (:require
   [clojure.string :as str]
   [clojure.test :as t]))

(def example-in (str/split-lines "1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"))

(defn smush-lines
  [lines]
  (->> lines
       (map #(str/split %1 #""))
       (mapv (fn [ln] (mapv #(Integer/parseInt %1) ln)))))

(defn get-coord
  {:test #(t/is (= 3 (get-coord '((2 1 9) (3 9 8)) {:x 0 :y 1})))}
  [grid c]
  (let [{x :x y :y} c]
    (nth (nth grid y nil) x nil)))

(defn points-around
  [{x :x y :y}]
;;   [{:x x :y (dec y)}
  [{:x x :y (inc y)}
;;    {:x (dec x) :y y}
   {:x (inc x) :y y}])

(defn get-paths
  [g pos visited]
  (cond
    (nil? pos) nil

    (and (= (pos :x) (dec (count g))) (= (pos :y) (dec (count g))))
    (lazy-seq (list (get-coord g pos) nil nil))

    :else (let [nxt (->> (points-around pos)
                         (filter (complement visited))
                         (filter #(some? (get-coord g %1))))]
            (lazy-seq (list
                       (get-coord g pos)
                       (get-paths g (first nxt) (conj visited pos))
                       (get-paths g (second nxt) (conj visited pos)))))))


(defn get-branch-totals
  [graph sum]
  ;; (prn (first graph) sum)
  (cond
    (nil? graph) sum
    :else (lazy-cat [(get-branch-totals (second graph) (+ sum (first graph)))
                     (get-branch-totals (last graph) (+ sum (first graph)))])))

(defn solve
  {:test #(t/is (= 40 (solve example-in)))}
  [lines]
  (let [grid (smush-lines lines)]
    (get-branch-totals (get-paths grid {:x 0 :y 0} #{}) 0)))

(t/run-tests)
