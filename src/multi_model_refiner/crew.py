import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI

load_dotenv()

os.environ["OPENAI_API_KEY"] = "lm-studio"
os.environ["OPENAI_API_BASE"] = "http://localhost:1234/v1"
os.environ["OPENAI_BASE_URL"] = "http://localhost:1234/v1" 

@CrewBase
class MultiModelRefinerCrew():
	"""MultiModelRefiner crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	llm = ChatOpenAI(
		openai_api_base="http://localhost:1234/v1",
		openai_api_key="lm-studio",
		model_name="phi-3-mini-4k-instruct"
	)

	@agent
	def crew1_researcher(self) -> Agent:
		return Agent(config=self.agents_config['crew1_researcher'], verbose=True, llm=self.llm)

	@agent
	def crew2_researcher(self) -> Agent:
		return Agent(config=self.agents_config['crew2_researcher'], verbose=True, llm=self.llm)

	@agent
	def refiner_arbiter(self) -> Agent:
		return Agent(config=self.agents_config['refiner_arbiter'], verbose=True, llm=self.llm)

	@task
	def primary_research_task(self) -> Task:
		return Task(config=self.tasks_config['primary_research_task'], agent=self.crew1_researcher())

	@task
	def secondary_research_task(self) -> Task:
		return Task(config=self.tasks_config['secondary_research_task'], agent=self.crew2_researcher())

	@task
	def refinement_task(self) -> Task:
		return Task(
			config=self.tasks_config['refinement_task'],
			agent=self.refiner_arbiter(),
			context=[self.primary_research_task(), self.secondary_research_task()],
            output_file='final_output.md'
		)

	@crew
	def crew(self) -> Crew:
		return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)