class Orchestrator:
    def __init__(self):
        self.agents = {}
        self.default_image_path = None
        self.default_caption = "Analyze this image and provide insights"
    
    def register_agent(self, name, agent):
        if name in self.agents:
            raise ValueError(f"Agent with name {name} already exists.")
        self.agents[name] = agent
        print(f"Registered agent: {name}")
    
    def get_agent(self, name):
        if name not in self.agents:
            raise ValueError(f"Agent with name {name} does not exist.")
        return self.agents[name]
    
    def list_agents(self):
        return list(self.agents.keys())
    
    def analyze_image(self, agent_name, image_path, caption="Analyze this image"):
        try:
            agent = self.get_agent(agent_name)
            if not hasattr(agent, 'analyze_image'):
                raise AttributeError(f"Agent {agent_name} does not have analyze_image method")
            return agent.analyze_image(image_path, caption)
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": agent_name
            }
    
    def create_image(self, agent_name, prompt):
        try:
            agent = self.get_agent(agent_name)
            if not hasattr(agent, 'create_image'):
                raise AttributeError(f"Agent {agent_name} does not have create_image method")
            return agent.create_image(prompt)
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": agent_name
            }
    
    def set_default_image_settings(self, image_path, caption=None):
        """Set default image path and caption for batch processing"""
        self.default_image_path = image_path
        if caption:
            self.default_caption = caption
    
    def run_process(self, image_path=None, caption=None):
        """
        Run the complete process: analyze image first, then create an image based on analysis
        """
        # Use provided parameters or defaults
        img_path = image_path or self.default_image_path
        img_caption = caption or self.default_caption
        
        if not img_path:
            return {
                "success": False,
                "error": "No image path provided and no default set"
            }
        
        results = {
            "analysis_results": [],
            "creation_results": [],
            "success": True
        }
        
        # Find analyzer and creator agents
        analyzer_agent = None
        creator_agent = None
        
        for agent_name, agent in self.agents.items():
            if hasattr(agent, 'analyze_image') and 'Analyzer' in agent_name:
                analyzer_agent = agent_name
            if hasattr(agent, 'create_image') and 'Creator' in agent_name:
                creator_agent = agent_name
        
        # Step 1: Analyze the image
        if analyzer_agent:
            print(f"Analyzing image with {analyzer_agent}...")
            analysis_result = self.analyze_image(analyzer_agent, img_path, img_caption)
            results["analysis_results"].append(analysis_result)
            print(f"Analysis result from {analyzer_agent}: {analysis_result}")
            
            # Step 2: Create an image based on the analysis
            if creator_agent and analysis_result.get("success"):
                analysis_text = analysis_result.get("analysis", "")
                print(f"Creating image with {creator_agent}...")
                created_image = self.create_image(creator_agent, analysis_text)
                results["creation_results"].append(created_image)
                print(f"Created image from {creator_agent}: {created_image.get('success', False)}")
            else:
                if not creator_agent:
                    results["creation_results"].append({
                        "success": False,
                        "error": "No creator agent found"
                    })
        else:
            results["analysis_results"].append({
                "success": False,
                "error": "No analyzer agent found"
            })
            results["success"] = False
        
        return results
    
    def get_agent_capabilities(self):
        """Return information about registered agents and their capabilities"""
        capabilities = {}
        for name, agent in self.agents.items():
            capabilities[name] = {
                "methods": [method for method in dir(agent) if not method.startswith('_')],
                "can_analyze": hasattr(agent, 'analyze_image'),
                "can_create": hasattr(agent, 'create_image')
            }
        return capabilities
