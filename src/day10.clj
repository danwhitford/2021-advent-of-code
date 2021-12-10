(ns day10
  (:require
   [clojure.string :as str]
   [clojure.test :as t]))

(def example-in (str/split-lines "[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"))

(def openers [\( \{ \[ \<])
(def closers [\) \} \] \>])
(def closers-map (zipmap openers closers))
(def score-map {\) 1
                \] 2
                \} 3
                \> 4})
(defn opener? [c] (some #{c} openers))
(defn closer? [c] (some #{c} closers))

(defn line-ok?
  {:test #(t/testing
           (t/is (= false (line-ok? "{([(<{}[<>[]}>{[]{[(<()>")))
            (t/is (= true (line-ok? "[(()[<>])]({[<{<<[]>>("))))}
  [line]
  (loop [[c & rst] line stk '()]
    (cond
      (nil? c) true
      (opener? c) (recur rst (conj stk c))
      (closer? c) (if (= c (closers-map (peek stk)))
                    (recur rst (pop stk))
                    false))))

(defn close-incomplete
  {:test #(t/is (= (seq "}}]])})]") (close-incomplete "[({(<(())[]>[[{[]{<()<>>")))}
  [line]
  (loop [[c & rst] line stk '()]
    (cond
      (nil? c) (map closers-map rst)
      (opener? c) (recur rst (conj stk c))
      (closer? c) (if (= c (closers-map (peek stk)))
                    (recur rst (pop stk))
                    nil))))

(defn sum-closers
  {:test #(t/is (= 294 (sum-closers '(\] \) \} \>))))}
  [closers]
  (reduce (fn [score ch] (+ (score-map ch) (* score 5))) 0 closers))

(defn middle [[fst & rst]]
  (if-not rst fst
          (recur (butlast rst))))

(defn solve
  {:test #(t/is (= 288957 (solve example-in)))}
  [lines]
  (->> lines       
       (map close-incomplete)
       (filter some?)
       (map sum-closers)
       (sort)
       (middle)))

(t/run-tests)
