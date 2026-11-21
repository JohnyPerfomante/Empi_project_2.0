import { Header, Notice, Panel, QueryState } from '../components/ui'
import { useApi } from '../lib/api'
import type { Configuration } from '../lib/types'

interface MethodologyData {
  algorithm_version: string
  formulas: { name: string; formula: string; description: string; origin: string }[]
  sources: { title: string; url: string; supports: string }[]
  configuration: Configuration
  example: { semantic: number; lexical: number; coverage: number; score: number }
  interpretation: string
  length_policy: string
}

export function Methodology() {
  const query = useApi<MethodologyData>('/analysis/methodology')
  const data = query.data
  return <>
    <Header title="Методика перевірки" eyebrow="ФОРМУЛИ ТА ДЖЕРЕЛА"
      subtitle="Як зіставляється зміст відповіді з кількома еталонами та формується рекомендація викладачу."/>
    <QueryState pending={query.isPending} error={query.error}/>
    {data && <>
      <Panel title={`Змістова перевірка · алгоритм ${data.algorithm_version}`}><div className="panel-body stack">
        <p>{data.length_policy}</p><p>{data.interpretation}</p>
        <p>Публікація питання потребує щонайменше двох різних еталонів. Непідтверджені варіації не беруть участі в аналізі.</p>
      </div></Panel>
      {data.formulas.map(formula => <Panel key={formula.name} title={formula.name}><div className="panel-body stack">
        <code className="formula-line">{formula.formula}</code><p>{formula.description}</p><p className="muted">Походження: {formula.origin}</p>
      </div></Panel>)}
      <Panel title="Поточні ваги та приклад"><div className="panel-body stack">
        <p>Вага семантики a = {data.configuration.semantic_weight}; лексики b = {data.configuration.lexical_weight}; понять c = {data.configuration.concept_weight}.</p>
        <code className="formula-line">F = {data.configuration.semantic_weight} × {data.example.semantic} + {data.configuration.lexical_weight} × {data.example.lexical} + {data.configuration.concept_weight} × {data.example.coverage} = {data.example.score}</code>
        <p>Це арифметичний приклад. У кожній картці аналізу використано її власні збережені метрики й налаштування, а не ці демонстраційні числа.</p>
        <p>Нижній поріг: {data.configuration.low_threshold}; високий поріг: {data.configuration.high_threshold}. Нижче нижнього порогу або за критичної суперечності — низька відповідність. До високого порогу, за нового заперечення або пропущених обов’язкових понять — потребує перевірки. Решта — висока відповідність.</p>
        <Notice>Зважене покриття, поєднання метрик, ваги та пороги — інженерні рішення цього проєкту. Вони не запозичені як готова формула оцінки з SBERT і потребують перевірки на корпусі з розміткою викладачів.</Notice>
      </div></Panel>
      <Panel title="Наукові та технічні першоджерела"><div className="panel-body stack">
        {data.sources.map(source => <div key={source.url}><a href={source.url} target="_blank" rel="noreferrer">{source.title}</a><p>{source.supports}</p></div>)}
      </div></Panel>
    </>}
  </>
}
