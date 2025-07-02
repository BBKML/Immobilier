from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Count, Q, Sum

def dashboard_stats(request):
    """
    Processeur de contexte pour fournir les statistiques détaillées du dashboard
    """
    if request.path.startswith('/admin/'):
        try:
            from django.db import connection
            
            # Vérifier si les tables existent
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vehicules_vehicule';")
                table_exists = cursor.fetchone()
                
            if not table_exists:
                # Si les tables n'existent pas, retourner des statistiques vides
                return {
                    'vehicules_count': 0,
                    'motos_count': 0,
                    'clients_count': 0,
                    'proprietaires_count': 0,
                    'marques_count': 0,
                    'types_vehicule_count': 0,
                    'types_moto_count': 0,
                    'vehicules_ce_mois': 0,
                    'motos_ce_mois': 0,
                    'tendance_vehicules': 0,
                    'tendance_motos': 0,
                    'top_marques': [],
                    'activite_recente': {'vehicules_recent': 0, 'motos_recent': 0},
                    'vehicules_actifs': 0,
                    'vehicules_inactifs': 0,
                    'motos_actives': 0,
                    'motos_inactives': 0,
                    'types_vehicule_stats': [],
                    'types_moto_stats': [],
                    'total_vehicules': 0,
                    'taux_activite_vehicules': 0,
                    'taux_activite_motos': 0,
                }
            
            # Si les tables existent, importer les modèles et calculer les statistiques
            from .models import Vehicule, Moto, Client, Proprietaire, Marque, TypeVehicule, TypeMoto
            
            today = timezone.now().date()
            this_month = today.replace(day=1)
            this_year = today.replace(month=1, day=1)
            last_month = (this_month - timedelta(days=1)).replace(day=1)
            
            # Statistiques de base
            vehicules_count = Vehicule.objects.count()
            motos_count = Moto.objects.count()
            clients_count = Client.objects.count()
            proprietaires_count = Proprietaire.objects.count()
            marques_count = Marque.objects.count()
            types_vehicule_count = TypeVehicule.objects.count()
            types_moto_count = TypeMoto.objects.count()
            
            # Statistiques temporelles
            vehicules_ce_mois = Vehicule.objects.filter(date__gte=this_month).count()
            motos_ce_mois = Moto.objects.filter(date__gte=this_month).count()
            vehicules_dernier_mois = Vehicule.objects.filter(date__gte=last_month, date__lt=this_month).count()
            motos_dernier_mois = Moto.objects.filter(date__gte=last_month, date__lt=this_month).count()
            
            # Calcul des tendances
            def calculer_tendance(actuel, precedent):
                if precedent == 0:
                    return 100 if actuel > 0 else 0
                return round(((actuel - precedent) / precedent) * 100, 1)
            
            tendance_vehicules = calculer_tendance(vehicules_ce_mois, vehicules_dernier_mois)
            tendance_motos = calculer_tendance(motos_ce_mois, motos_dernier_mois)
            
            # Top marques
            top_marques = Marque.objects.annotate(
                total_vehicules=Count('vehicule') + Count('moto')
            ).order_by('-total_vehicules')[:5]
            
            # Activité récente (7 derniers jours)
            activite_recente = {
                'vehicules_recent': Vehicule.objects.filter(date__gte=today - timedelta(days=7)).count(),
                'motos_recent': Moto.objects.filter(date__gte=today - timedelta(days=7)).count(),
            }
            
            # Statistiques par statut (si le champ existe)
            try:
                vehicules_actifs = Vehicule.objects.filter(statut='actif').count()
                vehicules_inactifs = Vehicule.objects.filter(statut='inactif').count()
                motos_actives = Moto.objects.filter(statut='actif').count()
                motos_inactives = Moto.objects.filter(statut='inactif').count()
            except:
                vehicules_actifs = vehicules_count
                vehicules_inactifs = 0
                motos_actives = motos_count
                motos_inactives = 0
            
            # Statistiques par type
            types_vehicule_stats = TypeVehicule.objects.annotate(
                count=Count('vehicule')
            ).order_by('-count')[:3]
            
            types_moto_stats = TypeMoto.objects.annotate(
                count=Count('moto')
            ).order_by('-count')[:3]
            
            return {
                # Statistiques de base
                'vehicules_count': vehicules_count,
                'motos_count': motos_count,
                'clients_count': clients_count,
                'proprietaires_count': proprietaires_count,
                'marques_count': marques_count,
                'types_vehicule_count': types_vehicule_count,
                'types_moto_count': types_moto_count,
                
                # Statistiques temporelles
                'vehicules_ce_mois': vehicules_ce_mois,
                'motos_ce_mois': motos_ce_mois,
                'tendance_vehicules': tendance_vehicules,
                'tendance_motos': tendance_motos,
                
                # Top marques
                'top_marques': top_marques,
                
                # Activité récente
                'activite_recente': activite_recente,
                
                # Statistiques par statut
                'vehicules_actifs': vehicules_actifs,
                'vehicules_inactifs': vehicules_inactifs,
                'motos_actives': motos_actives,
                'motos_inactives': motos_inactives,
                
                # Statistiques par type
                'types_vehicule_stats': types_vehicule_stats,
                'types_moto_stats': types_moto_stats,
                
                # Calculs dérivés
                'total_vehicules': vehicules_count + motos_count,
                'taux_activite_vehicules': round((vehicules_actifs / max(vehicules_count, 1)) * 100, 1),
                'taux_activite_motos': round((motos_actives / max(motos_count, 1)) * 100, 1),
            }
        except Exception as e:
            # En cas d'erreur, retourner des statistiques vides
            print(f"Error in dashboard_stats: {e}")
            return {
                'vehicules_count': 0,
                'motos_count': 0,
                'clients_count': 0,
                'proprietaires_count': 0,
                'marques_count': 0,
                'types_vehicule_count': 0,
                'types_moto_count': 0,
                'vehicules_ce_mois': 0,
                'motos_ce_mois': 0,
                'tendance_vehicules': 0,
                'tendance_motos': 0,
                'top_marques': [],
                'activite_recente': {'vehicules_recent': 0, 'motos_recent': 0},
                'vehicules_actifs': 0,
                'vehicules_inactifs': 0,
                'motos_actives': 0,
                'motos_inactives': 0,
                'types_vehicule_stats': [],
                'types_moto_stats': [],
                'total_vehicules': 0,
                'taux_activite_vehicules': 0,
                'taux_activite_motos': 0,
            }
    return {} 