"""
Pet behavior and interaction handlers
"""
import time
import random
import threading
from PyQt5.QtCore import QTimer, QPropertyAnimation, QPoint, QEasingCurve
from PyQt5.QtWidgets import QApplication


class PetBehavior:
    """Handles pet behaviors, interactions and AI responses"""
    
    def __init__(self, pet_instance):
        self.pet = pet_instance
        self.last_interaction_time = time.time()
        self.click_count = 0
        
        # Initialize timers
        self.running_timer = None
        self.action_timer = None
        self.speaking_check_timer = None
        
        # Initialize behavior systems
        self.start_behavior_timers()
    
    def start_behavior_timers(self):
        """Start all behavior timers"""
        # 🏃 Start random running timer (every 30 seconds)
        self.start_random_running()
        
        # 🎭 Start random action timer (every 45 seconds)
        self.start_random_actions()
        
        # 🤖 Start enhanced Gemini speaking system
        if self.pet.config.get("milk_mocha_speaking", True):
            self.start_smart_speaking_system()
        
        # 5️⃣ Start inactivity checking
        self.check_inactivity()
    
    def start_random_running(self):
        """Start the random running timer"""
        self.running_timer = QTimer()
        self.running_timer.timeout.connect(self.run_to_random_location)
        self.running_timer.start(30000)  # Run every 30 seconds
    
    def run_to_random_location(self):
        """Run to a random location on screen"""
        # Don't run if pet is drinking or angry
        if hasattr(self.pet, 'is_drinking') and self.pet.is_drinking:
            print("🥛 Pet is drinking - skipping random run")
            return
        
        if hasattr(self.pet, 'is_angry') and self.pet.is_angry:
            print("😡 Pet is angry - skipping random run")
            return
        
        # Get screen dimensions
        screen = QApplication.primaryScreen().availableGeometry()
        
        # Calculate random position (keeping pet within screen bounds)
        random_x = random.randint(0, screen.width() - self.pet.width())
        random_y = random.randint(0, screen.height() - self.pet.height())
        
        # Show running animation
        self.show_running(random_x, random_y)
    
    def show_running(self, target_x=None, target_y=None):
        """Show running animation and smoothly move to target location"""
        self.update_interaction_time()
        
        # Show running GIF (will loop until we stop it)
        self.pet.gif_manager.switch_gif("running", self.pet.pet_label)
        
        # If target coordinates provided, animate smoothly to target
        if target_x is not None and target_y is not None:
            # Stop and cleanup any existing animation
            if hasattr(self.pet, 'animation') and self.pet.animation:
                try:
                    self.pet.animation.finished.disconnect()
                    self.pet.animation.stop()
                except:
                    pass  # Ignore if already disconnected
            
            # Create smooth animation to target position
            self.pet.animation = QPropertyAnimation(self.pet, b"pos")
            self.pet.animation.setDuration(2000)  # 2 seconds for smooth movement
            self.pet.animation.setStartValue(QPoint(self.pet.x(), self.pet.y()))
            self.pet.animation.setEndValue(QPoint(target_x, target_y))
            self.pet.animation.setEasingCurve(QEasingCurve.OutQuad)  # Smooth deceleration
            
            # When animation finishes, stop running and return to idle
            self.pet.animation.finished.connect(self.finish_running)
            
            # Start the smooth animation
            self.pet.animation.start()
            print(f"🏃 Pet running smoothly to ({target_x}, {target_y})")
        else:
            # If no target, just show running for a short time
            QTimer.singleShot(3000, self.finish_running)
    
    def finish_running(self):
        """Finish running animation and return to idle"""
        # Stop running animation and return to idle
        self.pet.show_idle()
        
        # Save new position to config
        self.pet.config.update_position(self.pet.x(), self.pet.y())
        
        print("🏃 Pet finished running and returned to idle")
    
    def start_random_actions(self):
        """Start the random action timer"""
        if self.pet.config.get("auto_spawn", True):  # Only if auto_spawn is enabled
            self.action_timer = QTimer()
            self.action_timer.timeout.connect(self.perform_random_action)
            self.action_timer.start(45000)  # Random action every 45 seconds
    
    def perform_random_action(self):
        """Perform a random action animation"""
        # Don't perform random actions if pet is drinking or angry
        if hasattr(self.pet, 'is_drinking') and self.pet.is_drinking:
            print("🥛 Pet is drinking - skipping random action")
            return
        
        if hasattr(self.pet, 'is_angry') and self.pet.is_angry:
            print("😡 Pet is angry - skipping random action")
            return
            
        # Only perform random actions if currently idle
        if self.pet.gif_manager.current_gif == self.pet.gif_manager.gif_paths["idle"]:
            # Use pet's animation methods for random actions
            random_actions = [
                self.pet.show_dancing,
                self.pet.show_laugh,
                self.pet.show_excited,
                self.pet.show_heartthrow,
                self.pet.show_playing,
                self.pet.show_greeting,
                self.pet.show_says_yes,
                self.pet.show_doubtful
            ]
            action = random.choice(random_actions)
            action()
            print(f"🎭 Pet performed random action: {action.__name__}")
    
    def start_smart_speaking_system(self):
        """Start the enhanced speaking system with user activity detection"""
        speaking_interval = self.pet.config.get("speaking_interval", 15) * 60  # Convert to seconds
        print(f"🤖 Starting smart speaking system (interval: {speaking_interval//60} minutes)")
        
        # Check for speaking opportunities every 2 minutes
        self.speaking_check_timer = QTimer()
        self.speaking_check_timer.timeout.connect(self.check_speaking_opportunity)
        self.speaking_check_timer.start(120000)  # Check every 2 minutes
        
        # Also schedule a greeting message for startup
        QTimer.singleShot(5000, self.send_startup_greeting)  # 5 seconds after startup
    
    def check_speaking_opportunity(self):
        """Check if it's a good time to speak based on user activity"""
        speaking_enabled = self.pet.config.get("milk_mocha_speaking", True)
        speaking_interval = self.pet.config.get("speaking_interval", 15) * 60
        
        if not speaking_enabled:
            print("🔇 Speaking disabled")
            return
        
        # Check if enough time has passed since last message
        current_time = time.time()
        if self.pet.last_message_time and (current_time - self.pet.last_message_time) < speaking_interval:
            print(f"⏰ Too soon - last message was {current_time - self.pet.last_message_time:.1f} seconds ago")
            return
        
        print("✅ Time for a message!")
        # Check if user should receive a message
        if self.pet.user_activity.should_show_message(self.pet.last_message_time, speaking_interval):
            self.request_contextual_message()
        else:
            print("🚫 User activity detector says not a good time")
    
    def send_startup_greeting(self):
        """Send a contextual greeting message on startup"""
        print("🚀 send_startup_greeting called")
        speaking_enabled = self.pet.config.get("milk_mocha_speaking", True)
        if not speaking_enabled:
            print("🔇 Speaking disabled, skipping startup greeting")
            return
        
        time_context = self.pet.user_activity.get_time_context()
        context = "greetings" if time_context == "morning" else "random"
        print(f"🌅 Time context: {time_context}, using context: {context}")
        
        def get_greeting():
            print("🔄 Getting startup greeting in thread...")
            try:
                message = self.pet.gemini_service.get_message_with_timeout(context)
                print(f"✅ Got startup greeting: {message}")
                self.pet.show_speech_bubble(message)
                self.pet.last_message_time = time.time()
                print("✅ Startup greeting displayed immediately")
            except Exception as e:
                print(f"❌ Error getting startup greeting: {e}")
                import traceback
                traceback.print_exc()
                # Use simple fallback for startup
                self.pet.show_speech_bubble("🥛 Hello! Milk Mocha is ready to chat! Press G, B, or F for messages! ✨")
        
        thread = threading.Thread(target=get_greeting)
        thread.daemon = True
        thread.start()
        print("🧵 Startup greeting thread started")
    
    def request_contextual_message(self):
        """Request a contextual message based on user activity"""
        print("🎯 request_contextual_message called")
        
        def get_contextual_message():
            print("🔄 Getting contextual message in thread...")
            try:
                # Get user activity context
                activity_context = self.pet.user_activity.get_contextual_activity()
                print(f"🎯 Requesting message for context: {activity_context}")
                
                # Use the safe timeout method
                message = self.pet.gemini_service.get_contextual_message(activity_context)
                print(f"✅ Got contextual message: {message}")
                
                # Show message immediately
                self.pet.show_speech_bubble(message)
                self.pet.last_message_time = time.time()
                print("✅ Contextual message displayed immediately")
                
            except Exception as e:
                print(f"❌ Error getting contextual message: {e}")
                import traceback
                traceback.print_exc()
                # Last resort fallback
                try:
                    fallback = "🤖 Milk Mocha's AI is being shy! Press F for instant messages! 😊"
                    self.pet.show_speech_bubble(fallback)
                    print("✅ Emergency fallback displayed")
                except Exception as e2:
                    print(f"❌ Critical error: {e2}")
        
        # Show immediate feedback that something is happening
        self.pet.show_speech_bubble("🔄 Asking Gemini for a message... This might take a moment! 🤖")
        
        # Run in daemon thread to prevent blocking
        thread = threading.Thread(target=get_contextual_message)
        thread.daemon = True
        thread.start()
        print("🧵 Contextual message thread started")
    
    def request_custom_message(self, custom_prompt: str, context: str = "random"):
        """Request a custom message with specific prompt"""
        print(f"🎨 request_custom_message called with prompt: {custom_prompt}")
        
        def get_custom_message():
            print("🔄 Getting custom message in thread...")
            try:
                message = self.pet.gemini_service.get_message_with_timeout(context, custom_prompt)
                print(f"✅ Got custom message: {message}")
                self.pet.show_speech_bubble(message)
                self.pet.last_message_time = time.time()
                print("✅ Custom message displayed immediately")
            except Exception as e:
                print(f"❌ Error getting custom message: {e}")
                import traceback
                traceback.print_exc()
                try:
                    fallback = "🤖 Milk Mocha's creativity is blocked! Try the F key for instant quotes! 🎨"
                    self.pet.show_speech_bubble(fallback)
                    print("✅ Custom fallback displayed")
                except Exception as e2:
                    print(f"❌ Custom fallback failed: {e2}")
        
        # Show immediate feedback
        self.pet.show_speech_bubble("🎨 Creating a custom message... Hold on! ✨")
        
        thread = threading.Thread(target=get_custom_message)
        thread.daemon = True
        thread.start()
        print("🧵 Custom message thread started")
    
    def tell_funny_story(self):
        """Tell a short funny story generated by Gemini AI"""
        print("📚 tell_funny_story called")
        
        # Show thinking animation while generating story
        self.pet.show_watching_mobile()  # Show thinking animation
        self.update_interaction_time()
        
        def get_funny_story():
            print("� Getting funny story from Gemini in thread...")
            try:
                # Create a specific prompt for funny story generation
                story_prompt = (
                    "Tell a very short, funny story in just 1-2 sentences (under 30 words) from the perspective of "
                    "Milk Mocha, a cute desktop pet. Make it humorous about computer life. "
                    "Start with '📚' emoji and include one other emoji."
                )
                
                # Use the safe timeout method to get a story
                story = self.pet.gemini_service.get_message_with_timeout("random", story_prompt)
                print(f"✅ Got funny story: {story[:50]}...")
                
                # Switch to laugh animation when telling the story
                self.pet.show_laugh()
                
                # Show the story in a speech bubble
                self.pet.show_speech_bubble(story)
                self.pet.last_message_time = time.time()
                print("✅ Funny story displayed with laugh animation")
                
            except Exception as e:
                print(f"❌ Error getting funny story: {e}")
                import traceback
                traceback.print_exc()
                
                # Fallback to a pre-written story if Gemini fails
                fallback_stories = [
                    "📚 I tried to catch my cursor tail for 3 hours... I don't have one! 😅",
                    "� Made friends with antivirus software, but it called me 'suspicious'! 🛡️",
                    "📚 Spent all night dancing, your CPU hit 100% usage! 💃",
                    "� Tried to eat a pixel cookie, but it was just a cursor! 🍪",
                    "📚 Had an argument with Siri about who's cuter. I won! 😎"
                ]
                
                fallback_story = random.choice(fallback_stories)
                
                # Switch to laugh animation even for fallback stories
                self.pet.show_laugh()
                
                self.pet.show_speech_bubble(fallback_story)
                print(f"✅ Fallback story displayed with laugh animation: {fallback_story[:50]}...")
        
        # Show immediate feedback that story is being generated
        self.pet.show_speech_bubble("📚 Let me think of a funny story for you... 🤔✨")
        
        # Run story generation in daemon thread to prevent blocking
        thread = threading.Thread(target=get_funny_story)
        thread.daemon = True
        thread.start()
        print("🧵 Funny story generation thread started")
    
    def check_inactivity(self):
        """Check for inactivity and switch to sleeping if idle too long"""
        idle_time = time.time() - self.last_interaction_time
        if idle_time > 60:  # 1 minute of inactivity
            self.pet.show_sleeping()
        elif idle_time > 300:  # 5 minutes - show crying
            self.pet.show_crying()
        QTimer.singleShot(5000, self.check_inactivity)  # Check every 5 seconds
    
    def handle_click(self, event):
        """Handle left clicks with random reactions and spam protection"""
        try:
            self.click_count += 1
            self.update_interaction_time()
            
            if self.click_count >= 10:
                self.pet.show_angry()
                self.click_count = 0
            else:
                # Random reaction on click - call pet's animation methods
                reactions = [self.pet.show_excited, self.pet.show_laugh, self.pet.show_heartthrow]
                reaction = random.choice(reactions)
                reaction()  # Call the selected reaction
                print(f"🎭 Click reaction: {reaction.__name__}")
        except Exception as e:
            print(f"❌ Error in handle_click: {e}")
            import traceback
            traceback.print_exc()
    
    def pet_pet(self, event):
        """Handle right clicks to pet with heart throw"""
        try:
            self.update_interaction_time()
            self.pet.show_heartthrow()
            print("❤️ Pet petted with heart throw")
        except Exception as e:
            print(f"❌ Error in pet_pet: {e}")
            import traceback
            traceback.print_exc()
    
    def update_interaction_time(self):
        """Update the last interaction time"""
        self.last_interaction_time = time.time()
    
    def stop_timers(self):
        """Stop all behavior timers"""
        if self.running_timer:
            self.running_timer.stop()
        if self.action_timer:
            self.action_timer.stop()
        if self.speaking_check_timer:
            self.speaking_check_timer.stop()
